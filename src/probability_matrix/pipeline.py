from __future__ import annotations

from typing import Any, Dict

from src.common.io_utils import write_json


def run_stage4(panel_meta: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "stage": 4,
        "unsmoothed_cells": [],
        "smoothed_cells": [],
        "calibration": [],
        "note": "INSUFFICIENT DATA: no usable historical state prices from APIs in this environment.",
        "provisional": True,
    }
    write_json("outputs/stage4/probability_matrices.json", result)
    return result
