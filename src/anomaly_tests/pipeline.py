from __future__ import annotations

from typing import Dict

from src.common.io_utils import write_json


def run_stage8() -> Dict:
    payload = {
        "stage": 8,
        "confirmatory_tests": [],
        "exploratory_tests": [],
        "multiple_testing": "benjamini_hochberg_fdr",
        "status": "unavailable",
        "reason": "No validation outcomes estimable",
    }
    write_json("outputs/stage8/anomaly_report.json", payload)
    return payload
