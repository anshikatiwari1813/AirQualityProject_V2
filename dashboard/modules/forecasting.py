import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sys
import os

from tensorflow.keras.models import load_model
from database.save_prediction import save_prediction

# ======================================
# LOAD MODEL
# ======================================

@st.cache_resource
def load_lstm():

    model = load_model(
        "models/multivariate_lstm.keras"
    )

    feature_scaler = joblib.load(
        "models/feature_scaler.pkl"
    )

    target_scaler = joblib.load(
        "models/target_scaler.pkl"
    )

    return model, feature_scaler, target_scaler

model, feature_scaler, target_scaler = load_lstm()

# ======================================
# AQI CATEGORY
# ======================================

def get_aqi_category(aqi):

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

# ======================================
# HEALTH MESSAGE
# ======================================

def health_advisory(aqi):

    if aqi <= 50:
        return "Air quality is excellent."

    elif aqi <= 100:
        return "Air quality is acceptable."

    elif aqi <= 200:
        return "Sensitive people should reduce outdoor exposure."

    elif aqi <= 300:
        return "Avoid prolonged outdoor activities."

    elif aqi <= 400:
        return "Stay indoors whenever possible."

    else:
        return "Health emergency conditions."

# ======================================
# PAGE
# ======================================

def show_forecasting():

    st.title("📈 LSTM AQI Forecasting")

    st.markdown(
        """
        Upload your feature dataset and forecast
        the next AQI value using Multivariate LSTM.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload Feature Dataset CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.success(
            f"Dataset Loaded Successfully ({len(df)} rows)"
        )

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head()
        )

        features = [
            "PM2.5",
            "PM10",
            "NO2",
            "SO2",
            "CO",
            "O3",
            "Hour",
            "Day",
            "Month",
            "Year",
            "Season",
            "AQI_Lag_1",
            "AQI_Lag_6",
            "AQI_Lag_24",
            "AQI_Rolling_6",
            "AQI_Rolling_24"
        ]

        if st.button("🚀 Forecast AQI"):

            try:

                last_24 = df[
                    features
                ].tail(24)

                scaled = feature_scaler.transform(
                    last_24
                )

                X_input = np.array(
                    [scaled]
                )

                prediction = model.predict(
                    X_input
                )

                predicted_aqi = (
                    target_scaler
                    .inverse_transform(
                        prediction
                    )[0][0]
                )

                category = get_aqi_category(
                    predicted_aqi
                )

                
                category = get_aqi_category(
                    predicted_aqi
                )

                save_prediction(
                    "LSTM",
                    float(last_24["PM2.5"].iloc[-1]),
                    float(last_24["PM10"].iloc[-1]),
                    float(last_24["NO2"].iloc[-1]),
                    float(last_24["SO2"].iloc[-1]),
                    float(last_24["CO"].iloc[-1]),
                    float(last_24["O3"].iloc[-1]),
                    float(predicted_aqi),
                    category
                )

                st.success(
                    f"Forecasted AQI: {predicted_aqi:.2f}"
                )

                st.metric(
                    "Forecast Category",
                    category
                )

                st.warning(
                    health_advisory(
                        predicted_aqi
                    )
                )

                st.subheader(
                    "Last 24 Records Used"
                )

                st.dataframe(
                    last_24
                )

            except Exception as e:

                st.error(
                    f"Forecasting Error: {e}"
                )

    
    