import sqlite3

# =====================================
# CREATE DATABASE
# =====================================

conn = sqlite3.connect(
    "air_quality.db"
)

cursor = conn.cursor()

# =====================================
# AIR QUALITY DATA TABLE
# =====================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS air_quality_data (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    city TEXT,

    datetime TEXT,

    pm25 REAL,

    pm10 REAL,

    no2 REAL,

    so2 REAL,

    co REAL,

    o3 REAL,

    aqi REAL,

    hour INTEGER,

    day INTEGER,

    month INTEGER,

    year INTEGER,

    season INTEGER

)

""")

# =====================================
# PREDICTIONS TABLE
# =====================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    prediction_time TEXT,

    model_name TEXT,

    pm25 REAL,

    pm10 REAL,

    no2 REAL,

    so2 REAL,

    co REAL,

    o3 REAL,

    predicted_aqi REAL,

    category TEXT

)

""")

# =====================================
# LSTM FORECAST TABLE
# =====================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS forecasts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    forecast_time TEXT,

    model_name TEXT,

    predicted_aqi REAL,

    category TEXT

)

""")

# =====================================
# HEALTH ADVISORY TABLE
# =====================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS health_advisories (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    category TEXT,

    advisory TEXT

)

""")

# =====================================
# REPORTS TABLE
# =====================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS reports (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    generated_time TEXT,

    report_type TEXT,

    remarks TEXT

)

""")

# =====================================
# SAVE CHANGES
# =====================================

conn.commit()

# =====================================
# SHOW TABLES
# =====================================

cursor.execute(

    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """

)

tables = cursor.fetchall()

print("\nDatabase Created Successfully!\n")

print("Tables Created:\n")

for table in tables:

    print(table[0])

# =====================================
# CLOSE DATABASE
# =====================================

conn.close()

print("\nair_quality.db Ready To Use")