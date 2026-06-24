import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# =====================================
# LOAD MODEL
# =====================================

@st.cache_resource
def load_model():

    model = joblib.load(
        "models/best_aqi_model.pkl"
    )

    return model

model = load_model()

# =====================================
# PAGE
# =====================================

def show_explainability():

    st.title("🔍 Explainable AI (XAI)")

    st.markdown(
        """
        Understand which features influence AQI prediction
        using SHAP Explainability.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload Feature Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.success(
            f"Dataset Loaded ({len(df)} rows)"
        )

        st.subheader("Preview")

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
            "Weekday",
            "Season",
            "AQI_Lag_1",
            "AQI_Lag_6",
            "AQI_Lag_24",
            "AQI_Rolling_6",
            "AQI_Rolling_24"
        ]

        if st.button("Generate Explanation"):

            try:

                X = df[features].head(200)

                explainer = shap.TreeExplainer(
                    model
                )

                shap_values = explainer.shap_values(
                    X
                )

                st.subheader(
                    "Feature Importance"
                )

                fig, ax = plt.subplots()

                shap.summary_plot(
                    shap_values,
                    X,
                    show=False
                )

                st.pyplot(
                    plt.gcf()
                )

                st.success(
                    "Explanation Generated Successfully"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )