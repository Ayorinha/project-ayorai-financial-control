import pandas as pd
import pytest

from financial_control import build_state_summary, validate_and_enrich


def frame(**overrides):
    data = {
        "company": ["A", "B"],
        "state": ["SP", "RJ"],
        "issued": [100.0, 200.0],
        "received": [80.0, 150.0],
        "outstanding": [20.0, 50.0],
    }
    data.update(overrides)
    return pd.DataFrame(data)


def test_valid_data_calculates_collection_rate_and_status():
    out = validate_and_enrich(frame())
    assert out["collection_rate"].tolist() == [0.8, 0.75]
    assert out["status"].tolist() == ["PARTIAL", "PARTIAL"]


def test_rejects_missing_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_and_enrich(frame().drop(columns=["state"]))


def test_rejects_received_above_issued():
    with pytest.raises(ValueError, match="received cannot exceed issued"):
        validate_and_enrich(frame(received=[101.0, 150.0]))


def test_rejects_inconsistent_outstanding():
    with pytest.raises(ValueError, match="outstanding must equal"):
        validate_and_enrich(frame(outstanding=[99.0, 50.0]))


def test_state_summary():
    out = build_state_summary(validate_and_enrich(frame()))
    assert set(out["state"]) == {"SP", "RJ"}
    assert out["issued"].sum() == 300.0
