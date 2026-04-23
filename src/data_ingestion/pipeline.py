from __future__ import annotations

import os
from typing import Any, Dict

from src.common.http_utils import get_json
from src.common.io_utils import utc_now_iso, write_json


def run_stage1(config: Dict[str, Any]) -> Dict[str, Any]:
    out_dir = "outputs/stage1"
    os.makedirs(out_dir, exist_ok=True)

    apis = config["apis"]
    params = config["api_params"]
    cmc_key = os.environ.get(config["credentials"]["cmc_api_key_env"], config["credentials"]["cmc_api_key_fallback"])

    calls = {
        "polymarket_markets": (apis["polymarket_markets_url"], params["markets"], {}),
        "chainlink_btc_stream": (apis["chainlink_btc_stream_url"], {"network": "ethereum", "asset": "BTC", "format": "json"}, {}),
        "coinbase_btc_candles": (apis["coinbase_candles_url"], {"granularity": 60, "start": "2025-01-01T00:00:00Z", "end": "2025-01-02T00:00:00Z"}, {}),
        "cmc_fear_greed_latest": (apis["cmc_fear_greed_latest_url"], config["api_params"]["cmc_latest"], {"X-CMC_PRO_API_KEY": cmc_key}),
        "cmc_fear_greed_historical": (apis["cmc_fear_greed_historical_url"], config["api_params"]["cmc_historical"], {"X-CMC_PRO_API_KEY": cmc_key}),
        "pmxt_orderbooks": (apis["pmxt_url"], {"symbol": "BTC", "interval": "1h", "limit": 500}, {}),
    }

    coverage = {"stage": 1, "generated_utc": utc_now_iso(), "sources": {}}
    for name, (url, p, h) in calls.items():
        payload, err = get_json(url, p, headers=h, timeout=20)
        status = "ok" if err is None else "unavailable"
        sample_size = len(payload) if isinstance(payload, list) else (len(payload.keys()) if isinstance(payload, dict) else 0)
        coverage["sources"][name] = {
            "url": url,
            "params": p,
            "status": status,
            "error": err,
            "sample_size": sample_size,
            "provisional": status != "ok",
        }
        write_json(f"{out_dir}/{name}.json", payload if payload is not None else {"error": err, "url": url, "params": p})

    write_json(f"{out_dir}/coverage.json", coverage)
    return coverage
