import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from database.save_prediction import save_prediction
# ======================================
# LOAD MODEL
# ======================================

@st.cache_resource
def load_model():
    return joblib.load("models/best_aqi_model.pkl")

model = load_model()

explainer = shap.TreeExplainer(model)

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
# PAGE FUNCTION
# ======================================

def show_xgboost_prediction():

    st.title("⚡ XGBoost AQI Prediction")

    st.markdown(
        "Predict AQI using pollutant values and historical AQI features."
    )

    col1, col2 = st.columns(2)

    # ======================================
    # POLLUTANT INPUTS
    # ======================================

    with col1:

        pm25 = st.number_input(
            "PM2.5",
            min_value=0.0,
            value=80.0
        )

        pm10 = st.number_input(
            "PM10",
            min_value=0.0,
            value=150.0
        )

        no2 = st.number_input(
            "NO2",
            min_value=0.0,
            value=40.0
        )

        so2 = st.number_input(
            "SO2",
            min_value=0.0,
            value=20.0
        )

        co = st.number_input(
            "CO",
            min_value=0.0,
            value=1.0
        )

        o3 = st.number_input(
            "O3",
            min_value=0.0,
            value=35.0
        )

    # ======================================
    # DATE FEATURES
    # ======================================

    with col2:

        hour = st.slider(
            "Hour",
            0,
            23,
            12
        )

        day = st.slider(
            "Day",
            1,
            31,
            15
        )

        month = st.slider(
            "Month",
            1,
            12,
            6
        )

        year = st.slider(
            "Year",
            2015,
            2035,
            2024
        )

        weekday = st.slider(
            "Weekday",
            0,
            6,
            2
        )

    # ======================================
    # AUTO SEASON DETECTION
    # ======================================

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

    # ======================================
    # WEATHER CONTEXT
    # ======================================

    st.markdown("---")

    st.subheader("🌦 Weather Context")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Month",
            month
        )

    with c2:
        st.metric(
            "Season",
            season_name
        )

    with c3:
        st.metric(
            "Encoding",
            season
        )

    st.info(
        f"""
Season Encoding Used By Model

❄️ Winter = 1 (Dec-Feb)

☀️ Summer = 2 (Mar-May)

🌧️ Monsoon = 3 (Jun-Sep)

🍂 Post-Monsoon = 4 (Oct-Nov)

Current Selection:
Month {month} → {season_name}
"""
    )

    # ======================================
    # HISTORICAL AQI FEATURES
    # ======================================

    st.subheader("📈 Historical AQI Features")

    col3, col4, col5 = st.columns(3)

    with col3:

        aqi_lag_1 = st.number_input(
            "AQI Lag 1",
            value=150.0
        )

    with col4:

        aqi_lag_6 = st.number_input(
            "AQI Lag 6",
            value=145.0
        )

    with col5:

        aqi_lag_24 = st.number_input(
            "AQI Lag 24",
            value=140.0
        )

    col6, col7 = st.columns(2)

    with col6:

        aqi_roll_6 = st.number_input(
            "AQI Rolling 6",
            value=148.0
        )

    with col7:

        aqi_roll_24 = st.number_input(
            "AQI Rolling 24",
            value=142.0
        )

    # ======================================
    # AUTO PREDICTION
    # ======================================

    predict_clicked = True

    if predict_clicked:

        input_df = pd.DataFrame([{
            ...
        }])
    input_df = pd.DataFrame([{
        "PM2.5": pm25,
        "PM10": pm10,
        "NO2": no2,
        "SO2": so2,
        "CO": co,
        "O3": o3,
        "Hour": hour,
        "Day": day,
        "Month": month,
        "Year": year,
        "Weekday": weekday,
        "Season": season,
        "AQI_Lag_1": aqi_lag_1,
        "AQI_Lag_6": aqi_lag_6,
        "AQI_Lag_24": aqi_lag_24,
        "AQI_Rolling_6": aqi_roll_6,
        "AQI_Rolling_24": aqi_roll_24
    }])

    # Prediction
    prediction = float(
        model.predict(input_df)[0]
    )

    # SHAP values
    shap_values = explainer.shap_values(
        input_df
    )

    category = get_aqi_category(
        prediction
    )

    # Save to database
    save_prediction(
        "XGBoost",
        pm25,
        pm10,
        no2,
        so2,
        co,
        o3,
        prediction,
        category
    )

    # Prediction Result
    st.success(
        f"Predicted AQI: {prediction:.2f}"
    )

    st.metric(
        "AQI Category",
        category
    )

    st.subheader(
        "📋 Input Summary"
    )

    st.dataframe(
        input_df,
        width="stretch"
    )

    # ======================================
    # SHAP EXPLAINABILITY
    # ======================================

    st.markdown("---")

    st.subheader(
        "🧠 Explainable AI"
    )

    contributions = pd.DataFrame({

        "Feature": input_df.columns,

        "Contribution":
        shap_values[0].flatten()

    })

    st.dataframe(

        contributions.sort_values(
            by="Contribution",
            ascending=False
        ),

        width="stretch"

    )

    st.subheader(
        "📊 SHAP Visualization"
    )

    fig, ax = plt.subplots()

    shap.summary_plot(
        shap_values,
        input_df,
        show=False
    )

    st.pyplot(fig)