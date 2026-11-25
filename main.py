"""Run the full pipeline:  generate/load -> clean -> store -> analyse -> chart -> report."""
import argparse
from src import analysis, visualize
from src.cleaning import clean_expenses
from src.config import RAW_CSV, CURRENCY
from src.data_loader import load_csv
from src.database import save_to_sqlite
from src.generate_data import save_raw
from src.report import write_reports


def main():
    parser = argparse.ArgumentParser(description="Personal Expense Tracker")
    parser.add_argument("--csv", default=str(RAW_CSV), help="path to expense CSV")
    parser.add_argument("--regenerate", action="store_true", help="create new synthetic data")
    args = parser.parse_args()

    if args.regenerate or not RAW_CSV.exists():
        print("[1/6] Generating synthetic expense data ...")
        save_raw()
    else:
        print("[1/6] Using existing data file")

    print("[2/6] Loading CSV ...")
    raw = load_csv(args.csv)
    print(f"      {len(raw)} raw rows loaded")

    print("[3/6] Cleaning data ...")
    df, log = clean_expenses(raw)
    for key, val in log.items():
        print(f"      {key}: {val}")

    print("[4/6] Saving to SQLite ...")
    save_to_sqlite(df)

    print("[5/6] Analysing ...")
    k = analysis.key_metrics(df)
    print(f"      Total spend        : {CURRENCY}{k['total_spend']:,.0f}")
    print(f"      Avg daily spend    : {CURRENCY}{k['avg_daily_spend']:,.0f}")
    print(f"      Highest category   : {k['highest_category']}")
    print(f"      Highest-spend month: {k['highest_month']}")

    print("[6/6] Creating charts and reports ...")
    for path in visualize.make_all(df):
        print(f"      saved {path.name}")
    report = write_reports(df, log)
    print(f"      saved {report.name}")

    print("\nINSIGHTS")
    for line in analysis.generate_insights(df):
        print(f"  - {line}")


if __name__ == "__main__":
    main()
