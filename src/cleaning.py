"""Turn messy raw expense data into a clean, analysis-ready DataFrame."""
import pandas as pd
from .config import CATEGORY_ALIASES, PAYMENT_ALIASES, KEYWORD_RULES


def parse_dates(series):
    """Parse ISO dates first, then fall back to DD/MM/YYYY."""
    s = series.astype(str).str.strip()
    parsed = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    fallback = pd.to_datetime(s[parsed.isna()], format="%d/%m/%Y", errors="coerce")
    parsed.loc[fallback.index] = fallback
    return parsed


def guess_category(note):
    """Guess a category from keywords in the note."""
    text = str(note).lower()
    for category, words in KEYWORD_RULES.items():
        if any(w in text for w in words):
            return category
    return "Other"


def normalize_category(value):
    if pd.isna(value) or not str(value).strip():
        return None
    text = str(value).strip().lower()
    if text in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[text]
    return text.title().replace(" & ", " & ")


def clean_expenses(raw):
    """Return (clean_df, log). `log` records what was fixed - great for the README."""
    df = raw.copy()
    log = {"rows_raw": len(df)}

    df["date"] = parse_dates(df["date"])
    log["bad_dates_dropped"] = int(df["date"].isna().sum())
    df = df.dropna(subset=["date"])

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    bad = df["amount"].isna() | (df["amount"] <= 0)
    log["bad_amounts_dropped"] = int(bad.sum())
    df = df[~bad]

    df["category"] = df["category"].map(normalize_category)
    missing_cat = df["category"].isna()
    log["categories_auto_filled"] = int(missing_cat.sum())
    df.loc[missing_cat, "category"] = df.loc[missing_cat, "note"].map(guess_category)

    df["payment_method"] = (df["payment_method"].astype(str).str.strip().str.lower()
                            .map(PAYMENT_ALIASES).fillna("Other"))
    df["note"] = df["note"].fillna("No description").astype(str).str.strip()

    before = len(df)
    df = df.drop_duplicates()
    log["duplicates_removed"] = before - len(df)

    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["weekday"] = df["date"].dt.day_name()
    df = df.sort_values("date").reset_index(drop=True)
    log["rows_clean"] = len(df)
    return df, log
