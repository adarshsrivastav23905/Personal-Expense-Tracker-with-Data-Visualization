# Personal Expense Tracker with Data Visualization: Complete Guide

## 1. Project Explanation
**What is it?** A program that records everything you spend, organises it by category, and shows where your money goes.

**Problem solved:** People rarely know their real spending. Records are scattered, inconsistent and hard to read.

**Who benefits:** Students (allowance control), employees (savings goals), families (shared budgets), freelancers (irregular income, tax records), small businesses (cost tracking).

**How it helps:** Budgeting (limits per category), savings (income minus spend), spending control (alerts when over budget), planning (trends show what to cut).

**Simple explanation:** It is a smart notebook for money. You write expenses in; it tells you "you spent most on rent and food, and June was your costliest month."

**Technical explanation:** A Python ETL + analytics pipeline. Pandas cleans and aggregates; SQLite persists; Matplotlib/Seaborn render charts; a report module exports CSV/text; Streamlit optionally serves a dashboard.

**Workflow:** expense entry → storage → cleaning → category analysis → monthly analysis → visualization → report.

## 2. Tech Stack Options
| Option | Stack | Difficulty | Output |
|---|---|---|---|
| A Easy | Python, Pandas, CSV, Matplotlib | Beginner | Charts + CSV summary |
| B Intermediate | A + NumPy, Seaborn, SQLite, pytest, modular `src/` | Intermediate | Charts, DB, text report, tests |
| C Advanced | B + Streamlit, SQLAlchemy, scikit-learn classifier, Excel/PDF reports | Advanced | Interactive dashboard, ML categories |

**Best for students: Option B** (what this repo implements), with `app.py` as an optional taste of Option C. It shows more than a script but stays explainable in an interview.

## 3. Architecture
```
 Manual entry ─┐
 CSV file ─────┼─► data_loader.py ─► cleaning.py ─► database.py (SQLite)
 Synthetic ────┘   (generate_data.py)       │
                                            ▼
                                      analysis.py ─► visualize.py ─► images/*.png
                                            │
                                            └──────► report.py ───► outputs/*.csv, reports/*.txt
                                                         ▲
                                                  main.py / app.py
```
**Input:** date, category, amount, payment method, note.
**Processing:** read → clean → group by category/month → totals → top category → charts.
**Output:** category spend, monthly trend, payment analysis, savings summary, charts, reports.

## 4. Implementation Plan (10 phases)
| Phase | Do | Why | Expected output | Beginner mistake |
|---|---|---|---|---|
| 1 Setup | Install Python, venv, libraries | Isolated, reproducible environment | `pip list` shows libs | Skipping venv; wrong Python version |
| 2 Folders | Create structure | Clean GitHub repo | Folders exist | Everything in one file |
| 3 CSV creation | Run `generate_data.py` | No bank access needed | `data/expenses_raw.csv` | Forgetting `index=False` |
| 4 Loading | `data_loader.py` | One place to read data | DataFrame | Wrong relative paths |
| 5 Cleaning | `cleaning.py` | Garbage in, garbage out | Clean DataFrame + log | Not converting dates; ignoring duplicates |
| 6 Category analysis | `category_summary` | Shows where money goes | Table sorted by total | Forgetting to sort |
| 7 Monthly trend | `monthly_summary` | Reveals trend and savings | Month table | Sorting months as text with bad formats |
| 8 Visualization | `visualize.py` | Charts persuade | 5 PNGs | Unlabelled axes; overlapping labels |
| 9 Reports | `report.py` | Portable results | CSV + TXT | Overwriting results unknowingly |
| 10 GitHub | Commit and push | Proof of work | Public repo | Committing venv; no README |

## 5. Folder Structure
- `data/`: raw CSV, cleaned CSV, SQLite DB
- `notebooks/`: optional Jupyter exploration
- `src/`: reusable modules (one job per file)
- `tests/`: automated checks
- `outputs/`: generated summary CSVs
- `images/`: chart PNGs (shown in README)
- `reports/`: text report
- `docs/`: this guide
- `README.md`, `requirements.txt`, `.gitignore`, `main.py` (entry point), `app.py` (dashboard)

## 6. Installation
1. Install Python 3.9+ from python.org (tick "Add to PATH" on Windows). Check: `python --version`
2. Virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Libraries: `pip install -r requirements.txt`

## 7. Full Project Code
All code is in `src/`, `main.py`, `app.py` and `tests/`, fully commented. Covers synthetic data, CSV loading, cleaning, date conversion, category/monthly/payment analysis, highest category, average daily spend, 4 required charts (+ heatmap), reports.

## 8. Virtual Simulation
- **Records created:** `generate_data.py` loops over 6 months and, per category, creates a random number of transactions with random dates, amounts, payment methods and notes (fixed seed 42 so results repeat). Rent is fixed on the 1st.
- **Mess injected:** odd category text, missing categories/amounts/notes, `DD/MM/YYYY` dates, duplicates, to mimic real exports.
- **Categories assigned:** known categories are normalised via aliases; missing ones are guessed from note keywords (`swiggy` → Food & Dining).
- **Grouping:** `groupby("category")`, `groupby("month")`, `groupby("payment_method")`.
- **Monthly trends:** monthly totals, income minus spend = savings, month-over-month % change.
- **Overspending:** each month's category spend is compared with `BUDGETS` in `config.py`.
- **Charts:** Matplotlib/Seaborn save PNGs to `images/`.
- **Insights:** `generate_insights()` turns numbers into sentences.
- **Upload to GitHub:** `images/*.png`, `reports/expense_report.txt`, `outputs/*.csv`, `data/expenses_raw.csv`.

## 9. How to Run
```bash
python main.py
```
Expected terminal output (real run):
```
[1/6] Generating synthetic expense data ...
[2/6] Loading CSV ...        328 raw rows loaded
[3/6] Cleaning data ...      bad_amounts_dropped: 5, categories_auto_filled: 5,
                             duplicates_removed: 5, rows_clean: 318
[4/6] Saving to SQLite ...
[5/6] Analysing ...          Total spend Rs.149,380 | Avg daily Rs.825
                             Highest category: Rent | Highest month: 2026-06
[6/6] Creating charts and reports ...
```
**Generated:** 5 PNGs in `images/`, 4 CSVs in `outputs/`, `reports/expense_report.txt`, `data/expenses.db`.
**Sample insight:** "Average savings rate is 17.0%", but it fell from 32.7% in January to 4.0% in June as spending rose from Rs.20,205 to Rs.28,810. Food & Dining and Shopping repeatedly exceeded budget.

Note: Rent is the largest category but is fixed. In interviews, point out that Food & Dining (20.3%) is the largest *controllable* category.

## 10. GitHub Upload Steps
1. Create an account, then **New repository** (no README, since you already have one).
2. In your project folder:
```bash
git init
git add .
git commit -m "Initial commit: project structure"
git branch -M main
git remote add origin https://github.com/<your-username>/Personal-Expense-Tracker-Visualization.git
git push -u origin main
```
3. Later changes: `git add .` → `git commit -m "..."` → `git push`.
4. Upload screenshots by saving them in `images/` and committing them.

**Repo name:** `Personal-Expense-Tracker-Visualization`
**Description:** Python expense tracker: data cleaning, SQLite, budget alerts, Matplotlib/Seaborn charts and reports (Streamlit optional).
**Topics:** `python` `pandas` `data-analysis` `data-visualization` `matplotlib` `seaborn` `sqlite` `streamlit` `personal-finance` `expense-tracker`

## 11. README
See `README.md` in the repo root (copy-paste ready).

## 12. Proof-Building Plan (6 days)
| Day | Task | Commit message | Screenshots |
|---|---|---|---|
| 1 | Setup, folders, venv, requirements, .gitignore | `chore: set up project structure and requirements` | Folder tree |
| 2 | `config.py`, `generate_data.py`, `data_loader.py` | `feat: add synthetic expense data generator and loader` | Dataset preview |
| 3 | `cleaning.py`, `analysis.py`, tests | `feat: add data cleaning and analysis with tests` | Terminal output, `pytest` pass |
| 4 | Category charts and heatmap | `feat: add category-wise visualizations` | Bar chart, heatmap |
| 5 | Monthly, payment, daily charts | `feat: add monthly, payment and daily charts` | Line, pie, daily charts |
| 6 | `report.py`, README, docs, optional `app.py` | `docs: add report generation, README and guide` | Final report, GitHub repo page |

## 13. Screenshots to Capture
1. Project folder in VS Code explorer
2. `data/expenses_raw.csv` opened (first 15 rows)
3. Terminal after `python main.py`
4. `images/01_category_bar.png`
5. `images/02_monthly_line.png`
6. `images/03_payment_pie.png`
7. `images/04_daily_trend.png`
8. `reports/expense_report.txt`
9. GitHub repo page (README visible, charts rendered)
10. Optional: Streamlit dashboard

## 14. Interview Preparation
**Q1. Explain your project.**
I built a Python expense tracker. It takes expense data from CSV, manual entry or a synthetic generator, cleans it (fixes dates, categories, duplicates, missing values), stores it in SQLite, then analyses category-wise, monthly and payment-method spending. It draws charts, flags categories that exceed budget, and exports a report. In my sample data, savings fell from 32% to 4% in six months, and the tool made it obvious that food and shopping drove it.

**Q2. What problem does it solve?**
People spend without knowing where it goes. It makes spending visible and compares it with budgets.

**Q3. Which technologies did you use and why?**
Pandas for cleaning and aggregation, NumPy for random data generation, Matplotlib/Seaborn for charts, SQLite for lightweight persistence, pytest for tests, Streamlit for an optional dashboard.

**Q4. What data did you use?**
Synthetic data with date, category, amount, payment method and note, because I had no bank access. I deliberately added messy rows so cleaning was realistic.

**Q5. How did you clean the data?**
Parsed two date formats, converted amounts to numbers and dropped invalid ones, normalised category and payment spellings, auto-filled missing categories from note keywords, and removed duplicates. The pipeline logs how many rows each step affected.

**Q6. What analysis did you perform?**
Category totals and shares, monthly totals and savings rate, month-over-month change, payment-method split, average daily spend, highest category, and budget vs actual.

**Q7. Which charts and why?**
Bar for comparing categories, line for trends over time, pie for share by payment method, daily line with 7-day average to smooth noise, heatmap for category-by-month patterns.

**Q8. What challenges did you face?**
Mixed date formats, inconsistent categories, duplicates, and designing charts that are readable. I solved them with a staged cleaning function and tests.

**Q9. How would you improve it?**
Budget alerts by email, bank statement import, recurring-expense detection, an ML classifier for categories, multi-currency support and a deployed Streamlit app.

**Q10. Explain it to a non-technical person.**
It is like a smart notebook for money. You note what you spend, and it shows simple pictures of where the money goes and warns you when you spend too much.

**HR explanation (30 seconds):** "I built a tool that helps people understand and control their spending. It shows me I'm a good analyst and organised developer: I handled messy data, built charts, tested the code and documented it on GitHub."

**Technical explanation (30 seconds):** "Modular pipeline: loader → cleaner → SQLite → analysis functions → Matplotlib/Seaborn → report writer. Configuration is centralised, cleaning is unit-tested, and the same functions feed both the CLI and the Streamlit app."

**Be ready to say honestly:** the data is synthetic, and a duplicate rule that drops identical rows could, in real data, remove two genuine identical purchases. Adding a transaction ID would fix that.
