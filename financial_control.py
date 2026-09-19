from __future__ import annotations

from pathlib import Path
import pandas as pd

SAMPLE = [
    {"company":"Alpha","state":"SP","issued":10000,"received":8200,"outstanding":1800},
    {"company":"Beta","state":"RJ","issued":7500,"received":7500,"outstanding":0},
    {"company":"Gamma","state":"MG","issued":12000,"received":9000,"outstanding":3000},
]

def build_report(rows=SAMPLE) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df["collection_rate"] = (df["received"] / df["issued"]).fillna(0).round(4)
    df["status"] = df["outstanding"].map(lambda x: "OPEN" if x > 0 else "SETTLED")
    return df

def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)
    report = build_report()
    report.to_csv(out / "financial_report.csv", index=False)
    summary = report.groupby("state", as_index=False).agg(
        issued=("issued","sum"), received=("received","sum"), outstanding=("outstanding","sum")
    )
    summary.to_csv(out / "state_summary.csv", index=False)
    print(report.to_string(index=False))
    print("
State summary:")
    print(summary.to_string(index=False))
    print(f"
Reports written to {out.resolve()}")

if __name__ == "__main__":
    main()
