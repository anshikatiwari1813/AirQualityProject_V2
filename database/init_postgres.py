from sqlalchemy import text
from database.postgres_db import engine


def initialize_database():

    if engine is None:
        print("DATABASE_URL not found. Skipping PostgreSQL initialization.")
        return

    try:

        with engine.connect() as conn:

            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS predictions (

                id SERIAL PRIMARY KEY,

                prediction_time TIMESTAMP,

                model_name VARCHAR(100),

                pm25 FLOAT,
                pm10 FLOAT,
                no2 FLOAT,
                so2 FLOAT,
                co FLOAT,
                o3 FLOAT,

                predicted_aqi FLOAT,

                category VARCHAR(50)

            )
            """))

            conn.commit()

        print("PostgreSQL Database Initialized Successfully")

    except Exception as e:

        print(f"Database Initialization Error: {e}")