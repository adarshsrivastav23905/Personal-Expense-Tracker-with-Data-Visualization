"""Central settings: paths, budgets, and cleaning rules.
Change values here instead of hunting through the code."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
IMAGES_DIR = ROOT / "images"
REPORTS_DIR = ROOT / "reports"

RAW_CSV = DATA_DIR / "expenses_raw.csv"
CLEAN_CSV = DATA_DIR / "expenses_clean.csv"
DB_PATH = DATA_DIR / "expenses.db"

CURRENCY = "Rs."          # "Rs." avoids Unicode problems in Windows terminals
MONTHLY_INCOME = 30000    # student allowance / stipend (used for savings)

# Monthly budget per category (used to detect overspending)
BUDGETS = {
    "Rent": 6500, "Food & Dining": 4500, "Groceries": 3000,
    "Transport": 2000, "Shopping": 3000, "Entertainment": 1500,
    "Bills & Utilities": 1800, "Health": 1500, "Education": 2500,
}

# Fix inconsistent category spellings found in messy data
CATEGORY_ALIASES = {
    "food": "Food & Dining", "dining": "Food & Dining",
    "transportation": "Transport", "travel": "Transport",
    "utilities": "Bills & Utilities", "bills": "Bills & Utilities",
    "grocery": "Groceries",
}

PAYMENT_ALIASES = {
    "upi": "UPI", "cash": "Cash", "credit card": "Credit Card",
    "debit card": "Debit Card", "net banking": "Net Banking",
}

# If a category is missing, guess it from the note using keywords
KEYWORD_RULES = {
    "Food & Dining": ["swiggy", "zomato", "restaurant", "cafe", "coffee", "lunch", "dinner"],
    "Groceries": ["bazaar", "d-mart", "grocery", "supermart", "vegetables"],
    "Transport": ["uber", "ola", "metro", "petrol", "bus"],
    "Bills & Utilities": ["electric", "wifi", "broadband", "recharge", "water bill"],
    "Shopping": ["amazon", "flipkart", "myntra", "clothes"],
    "Entertainment": ["netflix", "spotify", "cinema", "bookmyshow", "movie"],
    "Health": ["pharmacy", "doctor", "medicine", "gym"],
    "Education": ["course", "book", "udemy", "stationery"],
    "Rent": ["rent", "hostel"],
}
