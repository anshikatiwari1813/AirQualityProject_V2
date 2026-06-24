import streamlit as st
import pandas as pd

def show_home():

    st.title("🌍 Air Quality Prediction & Monitoring System")

    st.markdown("""
    ### Smart Air Quality Analysis using Machine Learning & Deep Learning

    Predict AQI, Forecast Future Pollution Levels,
    Analyze Air Quality Trends and Generate Health Recommendations.
    """)

    st.success(
        "✅ System Ready | XGBoost + LSTM Models Successfully Integrated"
    )

    # =========================
    # METRICS
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Best Model",
            "XGBoost"
        )

    with col2:
        st.metric(
            "XGBoost R²",
            "0.7619"
        )

    with col3:
        st.metric(
            "LSTM Model",
            "Ready"
        )

    with col4:
        st.metric(
            "Records",
            "567K+"
        )

    st.divider()

    # =========================
    # FEATURES
    # =========================

    st.subheader("🚀 System Features")

    col1, col2 = st.columns(2)

    with col1:

        st.info("🤖 AQI Prediction using XGBoost")

        st.info("📈 AQI Forecasting using LSTM")

        st.info("🧮 AQI Calculator")

    with col2:

        st.info("🧠 Explainable AI")

        st.info("🏥 Health Advisory")

        st.info("📊 Interactive Dashboard")

    st.divider()

    # =========================
    # AQI CATEGORY TABLE
    # =========================

    st.subheader("🌫 AQI Categories")

    aqi_df = pd.DataFrame({

        "AQI Range": [
            "0-50",
            "51-100",
            "101-200",
            "201-300",
            "301-400",
            "401-500"
        ],

        "Category": [
            "Good 🟢",
            "Satisfactory 🟡",
            "Moderate 🟠",
            "Poor 🔴",
            "Very Poor 🟣",
            "Severe ⚫"
        ]
    })

    st.dataframe(
        aqi_df,
        use_container_width=True
    )

    st.divider()

    # =========================
    # FEATURE IMPORTANCE
    # =========================

    st.subheader("📊 Top AQI Influencing Factors")

    importance_df = pd.DataFrame({
        "Feature": [
            "PM2.5",
            "CO",
            "PM10",
            "Season",
            "Hour"
        ],
        "Importance": [
            55.8,
            12.9,
            10.1,
            5.8,
            3.7
        ]
    })

    st.bar_chart(
        importance_df.set_index("Feature")
    )

    st.divider()

    # =========================
    # WORKFLOW
    # =========================

    st.subheader("⚙ Project Workflow")

    st.markdown("""
    📂 Dataset Upload

    ⬇

    📊 Exploratory Data Analysis

    ⬇

    🧮 AQI Calculator

    ⬇

    🤖 XGBoost Prediction

    ⬇

    📈 LSTM Forecasting

    ⬇

    🧠 Explainable AI

    ⬇

    🏥 Health Advisory
    """)

    st.divider()

    st.markdown(
        """
        ### 👩‍💻 Developed By

        **Anshika Tiwari**

        Air Quality Prediction & Monitoring System

        Machine Learning | Deep Learning | Streamlit
        """
    )