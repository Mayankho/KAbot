from __future__ import annotations

import re
from typing import Dict, Tuple


THRESHOLD_PATTERNS = [
    re.compile(r"(?:price to beat|above|over|at least)\s*\$?([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"\$([0-9]{3,8}(?:\.[0-9]+)?)"),
]


def parse_threshold(text: str) -> Tuple[float | None, float, str]:
    if not text:
        return None, 0.0, "empty_text"
    for idx, pat in enumerate(THRESHOLD_PATTERNS):
        m = pat.search(text)
        if m:
            val = float(m.group(1))
            confidence = 0.9 if idx == 0 else 0.55
            return val, confidence, f"pattern_{idx+1}"
    return None, 0.0, "no_match"


def parse_market_threshold(market: Dict) -> Dict:
    text = " ".join(
        str(market.get(k, "")) for k in ["question", "title", "description", "rules", "slug"]
    )
    threshold, conf, method = parse_threshold(text)
    return {
        "threshold_price": threshold,
        "threshold_confidence": conf,
        "threshold_method": method,
        "threshold_text": text[:500],
    }
