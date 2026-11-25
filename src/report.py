"""Write CSV summaries and a plain-text report."""
from datetime import date
from .config import OUTPUT_DIR, REPORTS_DIR, CURRENCY, CLEAN_CSV
from . import analysis


def write_reports(df, log):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV, index=False)
    cats, months = analysis.category_summary(df), analysis.monthly_summary(df)
    pay, bud = analysis.payment_summary(df), analysis.budget_check(df)
    cats.to_csv(OUTPUT_DIR / "category_summary.csv", index=False)
    months.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)
    pay.to_csv(OUTPUT_DIR / "payment_summary.csv", index=False)
    bud.to_csv(OUTPUT_DIR / "budget_check.csv", index=False)

    k = analysis.key_metrics(df)
    lines = ["=" * 60, "PERSONAL EXPENSE TRACKER - SUMMARY REPORT",
             f"Generated: {date.today()}", "=" * 60, "",
             "KEY METRICS",
             f"  Period               : {k['period']}",
             f"  Total spend          : {CURRENCY}{k['total_spend']:,.2f}",
             f"  Transactions         : {k['transactions']}",
             f"  Avg daily spend      : {CURRENCY}{k['avg_daily_spend']:,.2f}",
             f"  Avg monthly spend    : {CURRENCY}{k['avg_monthly_spend']:,.2f}",
             f"  Highest category     : {k['highest_category']}",
             f"  Highest-spend month  : {k['highest_month']}", "",
             "DATA CLEANING LOG"]
    lines += [f"  {key:<24}: {val}" for key, val in log.items()]
    lines += ["", "CATEGORY SPENDING", cats.to_string(index=False), "",
              "MONTHLY SUMMARY", months.to_string(index=False), "",
              "PAYMENT METHODS", pay.to_string(index=False), "",
              "OVER-BUDGET ALERTS"]
    over = bud[bud["status"] == "OVER BUDGET"]
    lines.append(over.to_string(index=False) if len(over) else "  None")
    lines += ["", "INSIGHTS"] + [f"  - {t}" for t in analysis.generate_insights(df)]
    path = REPORTS_DIR / "expense_report.txt"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
