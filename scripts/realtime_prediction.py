import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pandas as pd
import joblib

from database.save_prediction import save_prediction
from alerts.email_alert import send_alert_email


print("Running Automated AQI Prediction...")


model = joblib.load(
    "models/pollutant_aqi_model.pkl"
)

df = pd.read_csv(
    "data/feature_dataset.csv"
)

latest = df.iloc[-1]

features = [
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3",
    "Hour",
    "Month",
    "Season"
]

input_df = pd.DataFrame(
    [latest[features]]
)

prediction =prediction = float(
    model.predict(input_df)[0]
)


def get_category(aqi):

    if aqi <= 50:
        return "Good 🟢"

    elif aqi <= 100:
        return "Satisfactory 🟡"

    elif aqi <= 200:
        return "Moderate 🟠"

    elif aqi <= 300:
        return "Poor 🔴"

    elif aqi <= 400:
        return "Very Poor 🟣"

    else:
        return "Severe ⚫"


category = get_category(
    prediction
)
if prediction > 200:

   send_alert_email(
    prediction,
    category,
    "anshika.tiwari1829@gmail.com"
)


save_prediction(
    "Auto-XGBoost",
    float(latest["PM2.5"]),
    float(latest["PM10"]),
    float(latest["NO2"]),
    float(latest["SO2"]),
    float(latest["CO"]),
    float(latest["O3"]),
    prediction,
    category
)

print(
    f"AQI Prediction Saved: {prediction:.2f}"
)