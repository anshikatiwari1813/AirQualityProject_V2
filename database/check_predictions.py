import sqlite3
import pandas as pd

conn = sqlite3.connect("air_quality.db")

df = pd.read_sql(
    "SELECT * FROM predictions ORDER BY id DESC",
    conn
)

conn.close()

print(df)