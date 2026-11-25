"""Create and save all charts as PNG files (headless-safe)."""
import matplotlib
matplotlib.use("Agg")  # no window needed; works on any machine
import matplotlib.pyplot as plt
import seaborn as sns
from .config import IMAGES_DIR, CURRENCY
from . import analysis

sns.set_theme(style="whitegrid")


def _save(fig, name):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGES_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def category_bar(df):
    s = analysis.category_summary(df)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=s, x="total", y="category", color="#4C72B0", ax=ax)
    for i, v in enumerate(s["total"]):
        ax.text(v, i, f" {CURRENCY}{v:,.0f}", va="center", fontsize=9)
    ax.set_title("Category-wise Spending")
    ax.set_xlabel(f"Total spend ({CURRENCY})"); ax.set_ylabel("")
    return _save(fig, "01_category_bar.png")


def monthly_line(df):
    m = analysis.monthly_summary(df)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(m["month"], m["total_spend"], marker="o", lw=2, label="Spending")
    ax.axhline(m["income"].iloc[0], color="green", ls="--", label="Income")
    for x, y in zip(m["month"], m["total_spend"]):
        ax.annotate(f"{y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center")
    ax.set_title("Monthly Spending Trend"); ax.set_ylabel(f"Spend ({CURRENCY})")
    ax.legend()
    return _save(fig, "02_monthly_line.png")


def payment_pie(df):
    p = analysis.payment_summary(df)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.pie(p["total"], labels=p["payment_method"], autopct="%1.1f%%", startangle=90,
           colors=sns.color_palette("pastel"))
    ax.set_title("Spending by Payment Method")
    return _save(fig, "03_payment_pie.png")


def daily_trend(df):
    d = analysis.daily_spending(df)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(d["date"], d["amount"], alpha=0.35, label="Daily spend")
    ax.plot(d["date"], d["rolling_7d_avg"], lw=2.5, color="#C44E52", label="7-day average")
    ax.set_title("Daily Spending Trend"); ax.set_ylabel(f"Spend ({CURRENCY})")
    ax.legend()
    return _save(fig, "04_daily_trend.png")


def category_heatmap(df):
    pivot = df.pivot_table(index="category", columns="month", values="amount",
                           aggfunc="sum", fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    ax.set_title("Spend Heatmap: Category x Month"); ax.set_xlabel(""); ax.set_ylabel("")
    return _save(fig, "05_category_month_heatmap.png")


def make_all(df):
    return [category_bar(df), monthly_line(df), payment_pie(df),
            daily_trend(df), category_heatmap(df)]
