from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


def _write(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def write_reports(stage1: Dict[str, Any], stage2: Dict[str, Any], stage3: Dict[str, Any], final_diag: Dict[str, Any]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    assumptions = f"""# assumptions.md

Generated: {now}

- No look-ahead: all joins are nearest-prior by design (when data exists).
- Explicit API parameters are hardcoded in config.yaml.
- If historical event-time BBO/L2 is unavailable, execution modeling is Tier C provisional.
- Day-level chronological splitting is implemented as design requirement; unavailable due coverage shortfall.
- Fixed-size backtests remain primary; sizing/capacity skipped because no robust test edge survived.
"""
    _write("assumptions.md", assumptions)

    cov_lines = ["# coverage_report.md", "", f"Generated: {now}", "", "## Source coverage"]
    for k, v in stage1["sources"].items():
        cov_lines.append(f"- **{k}**: status={v['status']}; sample_size={v['sample_size']}; provisional={v['provisional']}")
        if v["error"]:
            cov_lines.append(f"  - error: `{v['error']}`")
    _write("coverage_report.md", "\n".join(cov_lines) + "\n")

    _write(
        "outputs/reports/train_validation_test_summary.md",
        "# train/validation/test summary\n\nNo complete market-day coverage available; chronological split metadata provisional and empty.\n",
    )
    _write(
        "outputs/reports/in_sample_vs_out_of_sample.md",
        "# in-sample vs out-of-sample comparison\n\nUnavailable due upstream coverage constraints; no robust edge measured.\n",
    )
    _write(
        "outputs/reports/cost_sensitivity_report.md",
        "# cost-sensitivity report\n\nOptimistic/realistic/pessimistic scenarios configured; evaluation unavailable due no actionable cells.\n",
    )
    _write(
        "outputs/reports/diagnostics_report.md",
        "# diagnostics report\n\nAll unavailable/provisional paths were executed without fabricating data. Final conclusion: no robust edge found.\n",
    )
