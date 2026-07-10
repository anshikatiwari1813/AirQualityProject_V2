import streamlit as st
import pandas as pd
import os


def show_reports():

    st.title("📄 AQI Analysis Reports")

    st.markdown("""
    View model performance, feature importance,
    evaluation metrics and project summary.
    """)

    # =====================================
    # PROJECT SUMMARY
    # =====================================

    st.subheader("📌 Project Summary")

    st.info("""
### Air Quality Prediction and Monitoring System

**Machine Learning Models**
- 🌲 Random Forest Regressor (Current AQI Prediction)
- 🧠 Multivariate LSTM (AQI Forecasting)

### Major Features
- AQI Calculator
- Current AQI Prediction
- Future AQI Forecasting
- Explainable AI (SHAP)
- Health Advisory
- GIS Air Quality Map
- Hotspot Detection
- Prediction History
- Database Analytics
""")

    # =====================================
    # MODEL PERFORMANCE
    # =====================================

    st.subheader("🏆 Model Performance")

    performance = pd.DataFrame({

        "Model": [
            "Random Forest",
            "XGBoost",
            "Multivariate LSTM"
        ],

        "R² Score": [
            0.9872,
            0.9808,
            0.7176
        ],

        "MAE": [
            1.43,
            1.57,
            6.74
        ],

        "RMSE": [
            2.91,
            3.56,
            11.24
        ]

    })

    st.dataframe(
        performance,
        use_container_width=True
    )

    # =====================================
    # BEST MODELS
    # =====================================

    st.success(
        "🏆 Best AQI Prediction Model: Random Forest (R² = 0.9872)"
    )

    st.success(
        "📈 Forecasting Model: Multivariate LSTM (R² = 0.7176)"
    )

    # =====================================
    # FEATURE IMPORTANCE
    # =====================================

    st.subheader("📊 Feature Importance")

    feature_file = "feature_importance.csv"

    if os.path.exists(feature_file):

        importance = pd.read_csv(feature_file)

        st.dataframe(
            importance,
            use_container_width=True
        )

        st.bar_chart(
            importance.set_index("Feature")
        )

    else:

        st.warning(
            "Feature Importance file not found."
        )

    # =====================================
    # AQI CATEGORY TABLE
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

    st.subheader("⬇ Download Evaluation Report")

    csv = performance.to_csv(index=False)

    st.download_button(
        label="📥 Download Model Performance Report",
        data=csv,
        file_name="AQI_Model_Performance.csv",
        mime="text/csv"
    )