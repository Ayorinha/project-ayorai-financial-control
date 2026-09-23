from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd

REQUIRED_COLUMNS = ("company", "state", "issued", "received", "outstanding")
SAMPLE = [
    {"company": "Alpha", "state": "SP", "issued": 10000, "received": 8200, "outstanding": 1800},
    {"company": "Beta", "state": "RJ", "issued": 7500, "received": 7500, "outstanding": 0},
    {"company": "Gamma", "state": "MG", "issued": 12000, "received": 9000, "outstanding": 3000},
]


def build_report(rows: Iterable[Mapping[str, object]] = SAMPLE) -> pd.DataFrame:
    df = pd.DataFrame(list(rows))
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    for column in ("issued", "received", "outstanding"):
        df[column] = pd.to_numeric(df[column], errors="raise")
    if (df[["issued", "received", "outstanding"]] < 0).any().any():
        raise ValueError("financial amounts cannot be negative")
    if (df["received"] > df["issued"]).any():
        raise ValueError("received cannot exceed issued")
    if (df["outstanding"] != df["issued"] - df["received"]).any():
        raise ValueError("outstanding must equal issued - received")
    df["collection_rate"] = (df["received"] / df["issued"]).where(df["issued"] != 0, 0).round(4)
    df["status"] = df["outstanding"].map(lambda value: "OPEN" if value > 0 else "SETTLED")
    return df


def build_state_summary(report: pd.DataFrame) -> pd.DataFrame:
    return (
        report.groupby("state", as_index=False)
        .agg(issued=("issued", "sum"), received=("received", "sum"), outstanding=("outstanding", "sum"))
        .assign(collection_rate=lambda frame: (frame["received"] / frame["issued"]).where(frame["issued"] != 0, 0).round(4))
    )


def write_reports(report: pd.DataFrame, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "financial_report.csv"
    summary_path = output_dir / "state_summary.csv"
    report.to_csv(report_path, index=False)
    build_state_summary(report).to_csv(summary_path, index=False)
    return report_path, summary_path


def main() -> None:
    report = build_report()
    report_path, summary_path = write_reports(report, Path("output"))
    print(report.to_string(index=False))
    print("\nState summary:")
    print(build_state_summary(report).to_string(index=False))
    print(f"\nReports written to {report_path} and {summary_path}")


if __name__ == "__main__":
    main()
