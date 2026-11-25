"""Load expense data from a CSV file or add a record manually."""
import csv
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = ["date", "category", "amount", "payment_method", "note"]


def load_csv(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run `python main.py --regenerate` first.")
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")
    return df[REQUIRED_COLUMNS]


def add_manual_expense(path, date, category, amount, payment_method, note=""):
    """Append one expense row to the CSV (manual entry)."""
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([date, category, amount, payment_method, note])
