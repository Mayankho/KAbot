# assumptions.md

Generated: 2026-04-23T04:33:43.809568+00:00

- No look-ahead: all joins are nearest-prior by design (when data exists).
- Explicit API parameters are hardcoded in config.yaml.
- If historical event-time BBO/L2 is unavailable, execution modeling is Tier C provisional.
- Day-level chronological splitting is implemented as design requirement; unavailable due coverage shortfall.
- Fixed-size backtests remain primary; sizing/capacity skipped because no robust test edge survived.
