"""Interactive Streamlit dashboard for the Personal Expense Tracker."""
import pandas as pd
import streamlit as st

from src import analysis
from src.cleaning import clean_expenses
from src.config import CURRENCY, RAW_CSV
from src.data_loader import load_csv


@st.cache_data(ttl=300)
def load_default_expenses():
    raw = load_csv(RAW_CSV)
    return clean_expenses(raw)[0]


st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon=":material/account_balance_wallet:",
    layout="wide",
)

with st.sidebar:
    st.markdown("## :material/account_balance_wallet: Expense tracker")
    st.caption("Your spending, at a glance.")
    st.subheader("Your data")
    uploaded = st.file_uploader(
        "Upload expense CSV",
        type=["csv"],
        help="Required columns: date, category, amount, payment_method, note.",
    )

    with st.expander("Add a manual expense", icon=":material/add:"):
        with st.form("manual-expense"):
            expense_date = st.date_input("Date")
            category = st.text_input("Category", "Food & Dining")
            amount = st.number_input("Amount", min_value=1.0, step=100.0)
            payment_method = st.selectbox(
                "Payment method",
                ["UPI", "Cash", "Credit Card", "Debit Card", "Net Banking"],
            )
            note = st.text_input("Note", "Manual expense")
            submitted = st.form_submit_button(
                "Add expense",
                type="primary",
                icon=":material/add:",
                width="stretch",
            )

        if submitted:
            row = pd.DataFrame(
                [{
                    "date": expense_date.strftime("%Y-%m-%d"),
                    "category": category,
                    "amount": amount,
                    "payment_method": payment_method,
                    "note": note,
                }]
            )
            st.session_state.setdefault("manual_expenses", pd.DataFrame())
            st.session_state.manual_expenses = pd.concat(
                [st.session_state.manual_expenses, row],
                ignore_index=True,
            )
            st.toast("Expense added.", icon=":material/check_circle:")

if uploaded is not None:
    raw_df = pd.read_csv(uploaded)
    df, _ = clean_expenses(raw_df)
    data_source = uploaded.name
else:
    df = load_default_expenses()
    data_source = "Sample expense data"

manual_df = st.session_state.get("manual_expenses")
if manual_df is not None and not manual_df.empty:
    manual_clean, _ = clean_expenses(manual_df)
    df = pd.concat([df, manual_clean], ignore_index=True)
    df = df.drop_duplicates().sort_values("date").reset_index(drop=True)

months = ["All"] + sorted(df["month"].unique())
with st.sidebar:
    st.subheader("View")
    choice = st.selectbox("Reporting period", months)
    st.caption(f"Data source: {data_source}")

view = df if choice == "All" else df[df["month"] == choice]

st.markdown(":green-badge[:material/insights: PERSONAL FINANCE OVERVIEW]")
st.title("Your money, made clear.")
st.caption(
    f"Understand your spending patterns and stay on top of your budgets. "
    f"Showing **{choice if choice != 'All' else 'all months'}** · "
    f"{len(view):,} transactions · {data_source}"
)

if view.empty:
    st.info("No expenses found for this reporting period.")
    st.stop()

k = analysis.key_metrics(view)
monthly = analysis.monthly_summary(view)
daily = analysis.daily_spending(view)
category = analysis.category_summary(view)
payment = analysis.payment_summary(view)
budget = analysis.budget_check(view)
over_budget = budget[budget["status"] == "OVER BUDGET"]

metric_top = st.columns(2, gap="medium")
metric_top[0].metric(
    "Total spend",
    f"{CURRENCY}{k['total_spend']:,.0f}",
    border=True,
    help="Total recorded expenses in the selected reporting period.",
)
metric_top[1].metric(
    "Daily average",
    f"{CURRENCY}{k['avg_daily_spend']:,.0f}",
    border=True,
    help="Average spend per calendar day across the selected period.",
)
metric_bottom = st.columns(2, gap="medium")
metric_bottom[0].metric(
    "Transactions",
    f"{k['transactions']:,}",
    border=True,
    help="Number of cleaned transactions in the selected period.",
)
metric_bottom[1].metric(
    "Top category",
    k["highest_category"],
    border=True,
    help=f"{CURRENCY}{k['highest_category_total']:,.0f} recorded in this category.",
)

st.subheader("Spending insights")
st.caption("Explore where your money goes and how spending changes over time.")
left, right = st.columns(2, gap="medium")
with left:
    with st.container(border=True):
        st.markdown("#### :material/category: Spending by category")
        st.caption("Compare total expenses across categories.")
        st.bar_chart(
            category.set_index("category")["total"],
            horizontal=True,
        )

with right:
    with st.container(border=True):
        st.markdown("#### :material/trending_up: Monthly spending")
        st.caption("Track your total spend month by month.")
        st.line_chart(
            monthly.set_index("month")[["total_spend"]],
            x_label="Month",
            y_label=f"Spend ({CURRENCY})",
        )

left, right = st.columns(2, gap="medium")
with left:
    with st.container(border=True):
        st.markdown("#### :material/payments: Payment methods")
        st.caption("See which methods account for the most spend.")
        st.bar_chart(
            payment.set_index("payment_method")["total"],
            horizontal=True,
        )

with right:
    with st.container(border=True):
        st.markdown("#### :material/calendar_month: Daily spending")
        st.caption("Daily totals with a rolling seven-day average.")
        st.line_chart(
            daily.set_index("date")[["amount", "rolling_7d_avg"]],
            x_label="Date",
            y_label=f"Spend ({CURRENCY})",
        )

st.subheader("Budget health")
if budget.empty:
    st.caption("No configured budgets apply to this reporting period.")
else:
    if over_budget.empty:
        st.success("All tracked categories are within budget.", icon=":material/check_circle:")
    else:
        st.warning(
            f"{len(over_budget)} category-months are over budget.",
            icon=":material/warning:",
        )
    st.dataframe(
        budget,
        hide_index=True,
        column_config={
            "month": st.column_config.TextColumn("Month"),
            "category": st.column_config.TextColumn("Category"),
            "spend": st.column_config.NumberColumn(
                "Spend",
                format=f"{CURRENCY}%.2f",
            ),
            "budget": st.column_config.NumberColumn(
                "Budget",
                format=f"{CURRENCY}%.2f",
            ),
            "over_by": st.column_config.NumberColumn(
                "Over / under",
                format=f"{CURRENCY}%.2f",
            ),
            "status": st.column_config.TextColumn("Status"),
        },
    )

with st.expander("Review transactions", icon=":material/receipt_long:"):
    recent = view.sort_values("date", ascending=False).head(20)
    st.dataframe(
        recent[["date", "category", "amount", "payment_method", "note"]],
        hide_index=True,
        column_config={
            "date": st.column_config.DateColumn("Date", format="MMM D, YYYY"),
            "amount": st.column_config.NumberColumn(
                "Amount",
                format=f"{CURRENCY}%.2f",
            ),
        },
    )
