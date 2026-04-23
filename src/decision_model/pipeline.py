from __future__ import annotations

from typing import Any, Dict

from src.common.io_utils import write_json


def run_stage6() -> Dict[str, Any]:
    payload = {
        "stage": 6,
        "states": [],
        "validation_backtest": {
            "status": "unavailable",
            "reason": "No transition probabilities estimable with current data coverage",
            "provisional": True,
        },
    }
    write_json("outputs/stage6/sequential_decision_tables.json", payload)
    return payload
