"""Create a synthetic (fake but realistic) expense dataset, with a few
deliberate data-quality problems so the cleaning step has real work to do."""
import numpy as np
import pandas as pd
from .config import RAW_CSV

# category: (transactions per month, min amount, max amount, payment methods, notes)
SPEC = {
    "Food & Dining": ((16, 24), 80, 400, ["UPI", "Cash", "Credit Card"],
                      ["Swiggy order", "Zomato dinner", "Cafe coffee", "Restaurant lunch"]),
    "Groceries": ((4, 7), 150, 900, ["UPI", "Debit Card"],
                  ["D-Mart groceries", "Big Bazaar", "Vegetables", "Supermart"]),
    "Transport": ((8, 14), 30, 350, ["UPI", "Cash"],
                  ["Uber ride", "Ola cab", "Metro card", "Petrol", "Bus pass"]),
    "Shopping": ((2, 4), 300, 2200, ["Credit Card", "Net Banking", "UPI"],
                 ["Amazon order", "Flipkart sale", "Myntra clothes"]),
    "Entertainment": ((3, 6), 99, 500, ["UPI", "Credit Card"],
                      ["Netflix", "Spotify", "Cinema ticket", "BookMyShow"]),
    "Bills & Utilities": ((3, 4), 150, 700, ["UPI", "Net Banking"],
                          ["Mobile recharge", "WiFi bill", "Electricity bill"]),
    "Health": ((1, 2), 100, 900, ["UPI", "Cash"], ["Pharmacy", "Medicine", "Gym fee"]),
    "Education": ((1, 3), 150, 1200, ["UPI", "Credit Card"],
                  ["Udemy course", "Stationery", "Book purchase"]),
}


def generate_expenses(start="2026-01", months=6, seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for period in pd.period_range(start, periods=months, freq="M"):
        days = period.days_in_month
        rows.append((period.start_time.date(), "Rent", 6500.0, "UPI", "Hostel rent"))
        for cat, ((lo_n, hi_n), lo, hi, methods, notes) in SPEC.items():
            for _ in range(int(rng.integers(lo_n, hi_n + 1))):
                day = int(rng.integers(1, days + 1))
                amount = float(round(rng.integers(lo, hi + 1) / 5) * 5)
                rows.append((period.start_time.replace(day=day).date(), cat, amount,
                             str(rng.choice(methods)), str(rng.choice(notes))))
    df = pd.DataFrame(rows, columns=["date", "category", "amount", "payment_method", "note"])
    df = df.sort_values("date").reset_index(drop=True)
    return _add_mess(df, rng)


def _add_mess(df, rng):
    """Inject realistic problems: bad spelling, missing values, odd dates, duplicates."""
    df = df.copy()
    df["date"] = df["date"].astype(str)
    n = len(df)
    pick = lambda k: rng.choice(n, k, replace=False)
    for i in pick(12):                                   # messy category text
        df.loc[i, "category"] = f"  {str(df.loc[i, 'category']).lower()} "
    for i in pick(6):                                    # lowercase payment
        df.loc[i, "payment_method"] = str(df.loc[i, "payment_method"]).lower()
    for i in pick(5):                                    # missing category (note remains)
        df.loc[i, "category"] = np.nan
    for i in pick(5):                                    # missing/invalid amount
        df.loc[i, "amount"] = np.nan
    for i in pick(8):                                    # different date format
        d = pd.to_datetime(df.loc[i, "date"])
        df.loc[i, "date"] = d.strftime("%d/%m/%Y")
    for i in pick(5):                                    # missing note
        df.loc[i, "note"] = np.nan
    dupes = df.iloc[pick(5)]                             # duplicate rows
    return pd.concat([df, dupes], ignore_index=True)


def save_raw(path=RAW_CSV, **kwargs):
    path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_expenses(**kwargs)
    df.to_csv(path, index=False)
    return df
