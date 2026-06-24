import sqlite3

def get_connection():

    conn = sqlite3.connect(
        "air_quality.db",
        check_same_thread=False
    )

    return conn