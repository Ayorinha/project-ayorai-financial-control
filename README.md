# Project Ayorai — Financial Control

Runnable synthetic-data project demonstrating financial reconciliation and state-level analytics.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python financial_control.py
```

The script generates:

- `output/financial_report.csv`
- `output/state_summary.csv`

## Metrics

- issued amount
- received amount
- outstanding amount
- collection rate
- settlement status
- state-level aggregation

All sample data is fictitious. No institutional or personal financial data is included.

## Next engineering layer

The repository can later add a dashboard, database adapter, reconciliation rules and scheduled ingestion without changing the core analytical contract.

## Author

**Anderson Leon Ayora** — Data Scientist | AI Engineer | Data Architect
