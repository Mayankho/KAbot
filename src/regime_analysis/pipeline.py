from __future__ import annotations

from typing import Dict

from src.common.io_utils import write_json


def run_stage7() -> Dict:
    payload = {
        "stage": 7,
        "windows": ["earliest", "middle", "recent"],
        "drift": [],
        "equal_weight_vs_recency": "unavailable",
        "provisional": True,
    }
    write_json("outputs/stage7/stability_analysis.json", payload)
    return payload
