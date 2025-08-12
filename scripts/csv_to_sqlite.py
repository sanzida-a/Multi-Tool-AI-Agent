# scripts/csv_to_sqlite.py
import pandas as pd
import sqlite3
from pathlib import Path

def csv_to_sqlite(csv_path, db_path, table_name, if_exists='replace', chunksize=None):
    conn = sqlite3.connect(db_path)
    # Use pandas.to_sql for convenience
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False, chunksize=chunksize)
    conn.close()
    print(f"Wrote {csv_path} → {db_path} :: table {table_name}")

if __name__ == "__main__":
    csv_to_sqlite("data/csv_xlsx/heart_disease.csv", "data/databases/heart_disease.db", "heart_data")
    csv_to_sqlite("data/csv_xlsx/cancer.csv", "data/databases/cancer.db", "cancer_data")
    csv_to_sqlite("data/csv_xlsx/diabetes.csv", "data/databases/diabetes.db", "diabetes_data")
