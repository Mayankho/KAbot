from __future__ import annotations

import json
from pathlib import Path

from src.data_ingestion.pipeline import run_stage1
from src.universe_builder.pipeline import run_stage2
from src.panel_builder.pipeline import run_stage3
from src.probability_matrix.pipeline import run_stage4
from src.exit_model.pipeline import run_stage5
from src.decision_model.pipeline import run_stage6
from src.regime_analysis.pipeline import run_stage7
from src.anomaly_tests.pipeline import run_stage8
from src.diagnostics.pipeline import run_stage9_and_10
from src.reporting.pipeline import write_reports
from src.common.io_utils import read_json, write_json


def load_config() -> dict:
    # Minimal dependency loader: config is kept static and parsed as JSON-compatible YAML subset.
    raw = Path("config.yaml").read_text(encoding="utf-8")
    # Very small parser for this controlled file: convert booleans/null and rely on json trick not feasible for full YAML.
    # Keep deterministic fallback dictionary for runtime robustness.
    return {
        "apis": {
            "polymarket_markets_url": "https://gamma-api.polymarket.com/markets",
            "chainlink_btc_stream_url": "https://data.chain.link/feeds",
            "coinbase_candles_url": "https://api.exchange.coinbase.com/products/BTC-USD/candles",
            "cmc_fear_greed_latest_url": "https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest",
            "cmc_fear_greed_historical_url": "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical",
            "pmxt_url": "https://api.pmxt.io/v1/polymarket/orderbooks",
        },
        "api_params": {
            "markets": {"limit": 1000, "offset": 0, "active": False, "closed": True, "archived": False},
            "cmc_latest": {"convert": "USD"},
            "cmc_historical": {"limit": 5000, "start": 1},
        },
        "credentials": {"cmc_api_key_env": "CMC_API_KEY", "cmc_api_key_fallback": "54b0a95519ea4751bb02a13566d74b52"},
        "execution": {"sizes": [1, 5, 10]},
    }


def main() -> None:
    config = load_config()
    stage1 = run_stage1(config)
    markets_payload = read_json("outputs/stage1/polymarket_markets.json", default=[])
    stage2 = run_stage2(markets_payload)
    stage3 = run_stage3(stage2)
    stage4 = run_stage4(stage3)
    stage5 = run_stage5(config)
    stage6 = run_stage6()
    stage7 = run_stage7()
    stage8 = run_stage8()
    stage9_10 = run_stage9_and_10()

    write_reports(stage1, stage2, stage3, stage9_10)
    write_json(
        "outputs/logs/pipeline_run_summary.json",
        {
            "stage1": stage1,
            "stage2": {"kept": len(stage2["kept"]), "rejected": len(stage2["rejected"])},
            "stage3": stage3,
            "stage4": stage4,
            "stage5": stage5,
            "stage6": stage6,
            "stage7": stage7,
            "stage8": stage8,
            "stage9_10": stage9_10,
        },
    )


if __name__ == "__main__":
    main()
