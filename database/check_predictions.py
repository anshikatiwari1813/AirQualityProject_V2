from sqlalchemy import text
from database.postgres_db import engine
import pandas as pd

with engine.connect() as conn:

    df = pd.read_sql(
        text("SELECT * FROM predictions ORDER BY id DESC"),
        conn
    )

print(df)