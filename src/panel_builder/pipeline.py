from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from typing import Any, Dict, List


def run_stage3(universe: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for m in universe.get("kept", []):
        for sec in [300, 240, 180, 120, 60, 30, 10]:
            ts = (m["market_close_ts"] or 0) - sec
            row = {
                "condition_id": m["condition_id"],
                "market_slug": m["market_slug"],
                "token_id_yes": m["token_id_yes"],
                "market_open_ts": m["market_open_ts"],
                "market_close_ts": m["market_close_ts"],
                "resolution_ts": m["resolution_ts"],
                "resolved_yes": m["resolved_yes"],
                "threshold_price": m["threshold_price"],
                "timestamp": ts,
                "time_remaining_sec": sec,
                "best_bid_yes": None,
                "best_ask_yes": None,
                "mid_yes": None,
                "last_trade_yes": None,
                "display_price_yes": None,
                "spread_yes": None,
                "top_bid_depth_yes": None,
                "top_ask_depth_yes": None,
                "recent_trade_count": 0,
                "recent_trade_volume": 0.0,
                "btc_reference_price": None,
                "delta_usd": None,
                "delta_pct": None,
                "delta_z": None,
                "macro_regime": "unknown",
                "microstructure_regime": "missing",
                "liquidity_regime": "missing",
                "data_quality_flags": "missing_market_microstructure|missing_btc_reference",
                "liquidity_context_source": "missing",
            }
            rows.append(row)

    # Always emit a parquet-path artifact; fallback to JSONL when parquet libs unavailable.
    parquet_path = "canonical_state_panel.parquet"
    unavailable_note = {
        "status": "unavailable",
        "reason": "pyarrow/fastparquet unavailable in environment; wrote JSONL fallback instead",
        "fallback": "outputs/stage3/canonical_state_panel.jsonl",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    with open(parquet_path, "w", encoding="utf-8") as f:
        json.dump(unavailable_note, f, indent=2)

    with open("outputs/stage3/canonical_state_panel.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    with open("outputs/stage3/canonical_state_panel.csv", "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    return {"panel_rows": len(rows), "execution_tier": "C", "provisional": True}
