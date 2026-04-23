from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from src.common.io_utils import write_csv, write_json
from src.parsing.thresholds import parse_market_threshold


def _is_btc_5m_market(m: Dict[str, Any]) -> Tuple[bool, str]:
    text = " ".join(str(m.get(k, "")) for k in ["question", "title", "description", "slug"]).lower()
    if "btc" not in text and "bitcoin" not in text:
        return False, "not_btc"
    if "5 min" not in text and "5-minute" not in text and "5m" not in text:
        return False, "not_5m"
    return True, "ok"


def _to_ts(v: Any) -> int | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    try:
        dt = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
        return int(dt.timestamp())
    except Exception:
        return None


def run_stage2(markets_payload: Any) -> Dict[str, Any]:
    markets = markets_payload if isinstance(markets_payload, list) else []
    keep: List[Dict[str, Any]] = []
    reject: List[Dict[str, Any]] = []

    for m in markets:
        ok, reason = _is_btc_5m_market(m)
        if not ok:
            reject.append({"market_id": m.get("id"), "reason": reason})
            continue
        if not m.get("closed", False):
            reject.append({"market_id": m.get("id"), "reason": "unresolved_or_open"})
            continue
        parsed = parse_market_threshold(m)
        if parsed["threshold_price"] is None or parsed["threshold_confidence"] < 0.6:
            reject.append({"market_id": m.get("id"), "reason": "low_confidence_threshold", **parsed})
            continue

        yes_token = None
        tokens = m.get("tokens") or []
        for t in tokens:
            if str(t.get("outcome", "")).lower() == "yes":
                yes_token = t.get("token_id") or t.get("id")
                break
        if yes_token is None:
            reject.append({"market_id": m.get("id"), "reason": "missing_yes_token"})
            continue

        row = {
            "condition_id": m.get("conditionId") or m.get("condition_id") or m.get("id"),
            "market_slug": m.get("slug") or m.get("id"),
            "token_id_yes": yes_token,
            "market_open_ts": _to_ts(m.get("startDate") or m.get("open_time")),
            "market_close_ts": _to_ts(m.get("endDate") or m.get("close_time")),
            "resolution_ts": _to_ts(m.get("resolutionDate") or m.get("endDate")),
            "resolved_yes": 1 if str(m.get("outcome", "")).lower() == "yes" else 0,
            **parsed,
        }
        critical_missing = [k for k in ["market_open_ts", "market_close_ts", "resolution_ts"] if row[k] is None]
        if critical_missing:
            reject.append({"market_id": m.get("id"), "reason": f"missing_critical_fields:{','.join(critical_missing)}"})
            continue
        keep.append(row)

    default_fields = ["market_id", "reason", "threshold_price", "threshold_confidence", "threshold_method", "threshold_text"]
    dynamic_fields = sorted({k for r in reject for k in r.keys()})
    write_csv("reject_log.csv", reject, fieldnames=dynamic_fields or default_fields)
    write_json("outputs/stage2/market_universe.json", {"kept": len(keep), "rejected": len(reject), "rows": keep})
    return {"kept": keep, "rejected": reject}
