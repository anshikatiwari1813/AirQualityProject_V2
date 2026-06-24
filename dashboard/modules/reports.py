import streamlit as st
import pandas as pd
import os

def show_reports():

    st.title("📄 AQI Analysis Reports")

    st.markdown(
        """
        View model performance, feature importance
        and project summary reports.
        """
    )

    # =====================================
    # PROJECT SUMMARY
    # =====================================

    st.subheader("📌 Project Summary")

    st.info(
        """
        Air Quality Prediction and Monitoring System

        Models Used:
        • XGBoost (Current AQI Prediction)
        • Multivariate LSTM (AQI Forecasting)

        Features:
        • AQI Calculator
        • AQI Prediction
        • AQI Forecasting
        • Explainable AI
        • Health Advisory
        • EDA Dashboard
        """
    )

    # =====================================
    # MODEL PERFORMANCE
    # =====================================

    st.subheader("🏆 Model Performance")

    performance = pd.DataFrame({

        "Model": [
            "Random Forest",
            "XGBoost",
            "LSTM"
        ],

        "R² Score": [
            0.7570,
            0.7619,
            0.9676
        ],

        "MAE": [
            33.57,
            33.05,
            11.39
        ],

        "RMSE": [
            50.18,
            49.68,
            18.54
        ]

    })

    st.dataframe(
        performance,
        width="stretch"
    )

    # =====================================
    # BEST MODEL
    # =====================================

    st.success(
        "🏆 Best Forecasting Model: LSTM (R² = 0.9676)"
    )

    st.success(
        "🏆 Best AQI Prediction Model: XGBoost (R² = 0.7619)"
    )

    # =====================================
    # FEATURE IMPORTANCE
    # =====================================

    st.subheader("📊 Feature Importance")

    feature_file = (
        "models/pollutant_feature_importance.csv"
    )

    if os.path.exists(feature_file):

        importance = pd.read_csv(
            feature_file
        )

        st.dataframe(
            importance,
            width="stretch"
        )

        st.bar_chart(
            importance.set_index(
                "Feature"
            )
        )

    else:

        st.warning(
            "Feature Importance File Not Found"
        )

    # =====================================
    # AQI CATEGORIES
    # =====================================

    st.subheader("🌍 AQI Categories")

    category_df = pd.DataFrame({

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

    st.table(category_df)

    # =====================================
    # DOWNLOAD REPORT
    # =====================================

    st.subheader("⬇ Download Report")

    csv = performance.to_csv(
        index=False
    )

    st.download_button(
        label="Download Model Report",
        data=csv,
        file_name="AQI_Model_Report.csv",
        mime="text/csv"
    )