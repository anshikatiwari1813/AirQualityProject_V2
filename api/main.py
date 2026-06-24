from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(
    title="AQI Prediction API"
)

# Load model
model = joblib.load(
    "models/best_aqi_model.pkl"
)

@app.get("/")
def home():
    return {
        "message": "AQI Prediction API Running"
    }

@app.post("/predict")
def predict(
    pm25: float,
    pm10: float,
    no2: float,
    so2: float,
    co: float,
    o3: float,
    hour: int,
    day: int,
    month: int,
    year: int,
    weekday: int,
    season: int,
    aqi_lag1: float,
    aqi_lag6: float,
    aqi_lag24: float,
    aqi_roll6: float,
    aqi_roll24: float
):

    data = pd.DataFrame([[
        pm25,
        pm10,
        no2,
        so2,
        co,
        o3,
        hour,
        day,
        month,
        year,
        weekday,
        season,
        aqi_lag1,
        aqi_lag6,
        aqi_lag24,
        aqi_roll6,
        aqi_roll24
    ]])

    prediction = model.predict(data)

    return {
        "Predicted_AQI": round(
            float(prediction[0]), 2
        )
    }