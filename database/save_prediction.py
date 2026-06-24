import sqlite3
from datetime import datetime


def save_prediction(
    model_name,
    pm25,
    pm10,
    no2,
    so2,
    co,
    o3,
    predicted_aqi,
    category
):

    predicted_aqi = float(predicted_aqi)

    conn = sqlite3.connect(
        "air_quality.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (

            prediction_time,
            model_name,

            pm25,
            pm10,
            no2,
            so2,
            co,
            o3,

            predicted_aqi,
            category

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            model_name,

            pm25,
            pm10,
            no2,
            so2,
            co,
            o3,

            predicted_aqi,
            category
        )
    )

    conn.commit()
    conn.close()