import pandas as pd
from src.cleaning import clean_expenses, parse_dates, guess_category


def test_mixed_date_formats():
    out = parse_dates(pd.Series(["2026-01-05", "06/01/2026"]))
    assert out.iloc[0] == pd.Timestamp("2026-01-05")
    assert out.iloc[1] == pd.Timestamp("2026-01-06")


def test_guess_category():
    assert guess_category("Swiggy order") == "Food & Dining"
    assert guess_category("???") == "Other"


def test_clean_removes_bad_rows_and_duplicates():
    raw = pd.DataFrame({
        "date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03"],
        "category": ["  food ", "  food ", None, "Shopping"],
        "amount": [100, 100, 250, "abc"],
        "payment_method": ["upi", "upi", "CASH", "UPI"],
        "note": ["Lunch", "Lunch", "Uber ride", "x"],
    })
    df, log = clean_expenses(raw)
    assert len(df) == 2
    assert set(df["category"]) == {"Food & Dining", "Transport"}
    assert log["duplicates_removed"] == 1
    assert log["bad_amounts_dropped"] == 1
