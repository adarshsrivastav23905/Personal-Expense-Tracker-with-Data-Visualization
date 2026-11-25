"""Store cleaned expenses in SQLite so they can be queried with SQL."""
import sqlite3
import pandas as pd
from .config import DB_PATH


def save_to_sqlite(df, db_path=DB_PATH):
    out = df.copy()
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    with sqlite3.connect(db_path) as con:
        out.to_sql("expenses", con, if_exists="replace", index=False)


def run_query(sql, db_path=DB_PATH):
    with sqlite3.connect(db_path) as con:
        return pd.read_sql_query(sql, con)
