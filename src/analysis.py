"""All the numbers: category, monthly, payment-method, daily, budget analysis."""
import pandas as pd
from .config import BUDGETS, MONTHLY_INCOME, CURRENCY


def category_summary(df):
    g = df.groupby("category")["amount"].agg(total="sum", transactions="count", average="mean")
    g["share_pct"] = g["total"] / g["total"].sum() * 100
    return g.sort_values("total", ascending=False).round(2).reset_index()


def monthly_summary(df):
    m = df.groupby("month")["amount"].agg(total_spend="sum", transactions="count").reset_index()
    m["income"] = MONTHLY_INCOME
    m["savings"] = m["income"] - m["total_spend"]
    m["savings_rate_pct"] = m["savings"] / m["income"] * 100
    m["mom_change_pct"] = m["total_spend"].pct_change() * 100
    return m.round(2)


def payment_summary(df):
    p = df.groupby("payment_method")["amount"].agg(total="sum", transactions="count")
    p["share_pct"] = p["total"] / p["total"].sum() * 100
    return p.sort_values("total", ascending=False).round(2).reset_index()


def daily_spending(df):
    """Total spend per calendar day (days with no spending count as 0)."""
    daily = df.groupby("date")["amount"].sum()
    full = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(full, fill_value=0).rename_axis("date").reset_index()
    daily["rolling_7d_avg"] = daily["amount"].rolling(7, min_periods=1).mean()
    return daily


def budget_check(df):
    """Compare each month's category spend with its budget."""
    spend = df.groupby(["month", "category"])["amount"].sum().reset_index(name="spend")
    spend["budget"] = spend["category"].map(BUDGETS)
    spend = spend.dropna(subset=["budget"])
    spend["over_by"] = spend["spend"] - spend["budget"]
    spend["status"] = spend["over_by"].apply(lambda x: "OVER BUDGET" if x > 0 else "OK")
    return spend.sort_values(["month", "over_by"], ascending=[True, False]).round(2)


def key_metrics(df):
    days = (df["date"].max() - df["date"].min()).days + 1
    cats = category_summary(df)
    months = monthly_summary(df)
    return {
        "period": f"{df['date'].min().date()} to {df['date'].max().date()}",
        "total_spend": df["amount"].sum(),
        "transactions": len(df),
        "avg_daily_spend": df["amount"].sum() / days,
        "avg_monthly_spend": months["total_spend"].mean(),
        "highest_category": cats.iloc[0]["category"],
        "highest_category_total": cats.iloc[0]["total"],
        "highest_month": months.loc[months["total_spend"].idxmax(), "month"],
        "avg_savings_rate_pct": months["savings_rate_pct"].mean(),
    }


def generate_insights(df):
    """Plain-English findings for the final report."""
    k, cats, pay = key_metrics(df), category_summary(df), payment_summary(df)
    bud = budget_check(df)
    over = bud[bud["status"] == "OVER BUDGET"]
    insights = [
        f"Total spending was {CURRENCY}{k['total_spend']:,.0f} over {k['period']}.",
        f"'{k['highest_category']}' is the biggest category "
        f"({CURRENCY}{k['highest_category_total']:,.0f}, "
        f"{cats.iloc[0]['share_pct']:.1f}% of spend).",
        f"Average daily spend is {CURRENCY}{k['avg_daily_spend']:,.0f}; "
        f"the costliest month was {k['highest_month']}.",
        f"'{pay.iloc[0]['payment_method']}' is the most used payment method "
        f"({pay.iloc[0]['share_pct']:.1f}% of spend).",
        f"Average savings rate: {k['avg_savings_rate_pct']:.1f}% of income.",
    ]
    if len(over):
        worst = over.sort_values("over_by", ascending=False).iloc[0]
        insights.append(f"{len(over)} category-months went over budget; the worst was "
                        f"{worst['category']} in {worst['month']} "
                        f"(over by {CURRENCY}{worst['over_by']:,.0f}).")
    else:
        insights.append("No category went over its budget.")
    return insights
