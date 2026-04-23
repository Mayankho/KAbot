from __future__ import annotations

from typing import Any, Dict

from src.common.io_utils import write_json


def run_stage5(config: Dict[str, Any]) -> Dict[str, Any]:
    tables = []
    for size in config["execution"]["sizes"]:
        tables.append({
            "size": size,
            "tier": "C",
            "immediate_exit_prob": None,
            "future_exit_prob": None,
            "provisional": True,
            "note": "Trade/history-only proxy unavailable due missing trade history ingestion.",
        })
    payload = {"stage": 5, "rows": tables, "provisional": True}
    write_json("outputs/stage5/exit_probability_tables.json", payload)
    return payload
