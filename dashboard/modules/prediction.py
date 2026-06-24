import streamlit as st
import pandas as pd
import joblib


# ======================================
# LOAD RANDOM FOREST MODEL
# ======================================

@st.cache_resource
def load_model():
    return joblib.load("models/pollutant_aqi_model.pkl")

model = load_model()

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
# HEALTH ADVISORY
# ======================================

def health_advisory(aqi):

    if aqi <= 50:
        return "Air quality is excellent. Safe for outdoor activities."

    elif aqi <= 100:
        return "Air quality is acceptable."

    elif aqi <= 200:
        return "Sensitive individuals should reduce prolonged outdoor exposure."

    elif aqi <= 300:
        return "Avoid prolonged outdoor activities."

    elif aqi <= 400:
        return "Stay indoors as much as possible."

    else:
        return "Health emergency conditions. Avoid going outside."


# ======================================
# MAIN PAGE
# ======================================

def show_prediction():

    st.title("🌳 Random Forest AQI Prediction")

    col1, col2 = st.columns(2)

    with col1:

        pm25 = st.number_input("PM2.5", min_value=0.0, value=80.0)

        pm10 = st.number_input("PM10", min_value=0.0, value=150.0)

        no2 = st.number_input("NO2", min_value=0.0, value=40.0)

        so2 = st.number_input("SO2", min_value=0.0, value=20.0)

    with col2:

        co = st.number_input("CO", min_value=0.0, value=1.0)

        o3 = st.number_input("O3", min_value=0.0, value=35.0)

        hour = st.slider("Hour", 0, 23, 12)

        month = st.slider("Month", 1, 12, 6)

    # Season Detection

    if month in [12, 1, 2]:
        season = 1
        season_name = "Winter ❄️"

    elif month in [3, 4, 5]:
        season = 2
        season_name = "Summer ☀️"

    elif month in [6, 7, 8, 9]:
        season = 3
        season_name = "Monsoon 🌧️"

    else:
        season = 4
        season_name = "Post-Monsoon 🍂"

    st.info(f"Detected Season: {season_name} (Code = {season})")

    if st.button("🚀 Predict AQI"):

        input_df = pd.DataFrame({
            "PM2.5": [pm25],
            "PM10": [pm10],
            "NO2": [no2],
            "SO2": [so2],
            "CO": [co],
            "O3": [o3],
            "Hour": [hour],
            "Month": [month],
            "Season": [season]
        })

        prediction = model.predict(input_df)[0]

        st.success(f"Predicted AQI: {prediction:.2f}")

        st.metric(
            "AQI Category",
            get_aqi_category(prediction)
        )

        st.warning(
            health_advisory(prediction)
        )

        st.subheader("Input Data")

        st.dataframe(input_df)

