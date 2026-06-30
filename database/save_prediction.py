from datetime import datetime
from sqlalchemy import text
from database.postgres_db import engine


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

    with engine.connect() as conn:

        conn.execute(
            text("""
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

            VALUES (

                :prediction_time,
                :model_name,

                :pm25,
                :pm10,
                :no2,
                :so2,
                :co,
                :o3,

                :predicted_aqi,
                :category

            )
            """),

            {

                "prediction_time": datetime.now(),

                "model_name": model_name,

                "pm25": pm25,
                "pm10": pm10,
                "no2": no2,
                "so2": so2,
                "co": co,
                "o3": o3,

                "predicted_aqi": float(predicted_aqi),

                "category": category
            }
        )

        conn.commit()