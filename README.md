# KAbot - Polymarket BTC 5m Research Pipeline

Reproducible, conservative, stage-structured research pipeline for Polymarket Bitcoin 5-minute up/down binaries.

## Run

```bash
python run_pipeline.py
```

## Design highlights

- Strict no-look-ahead design intent (nearest-prior alignment only).
- Explicit API parameters (no hidden defaults in request construction).
- Chronological train/validation/test logic guarded by day boundaries.
- Tiered execution data model:
  - Tier A event-time book data
  - Tier B coarse snapshots
  - Tier C trade/price proxy (provisional)
- Graceful degradation when APIs are unavailable.

## Outputs

- `config.yaml`
- `hypotheses_registry.yaml`
- `assumptions.md`
- `coverage_report.md`
- `reject_log.csv`
- `canonical_state_panel.parquet` (fallback note + JSONL/CSV in `outputs/stage3/` when parquet libs unavailable)
- stage artifacts under `outputs/stage*/`
- report artifacts under `outputs/reports/`

Final conclusion is written to `outputs/stage9_10/heldout_and_extensions.json`.
