import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import numpy as np

# =====================================
# LOAD MODEL
# =====================================

@st.cache_resource
def load_model():

    return joblib.load(
        "models/best_aqi_model.pkl"
    )


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

    if uploaded_file is None:
        return

    try:

        df = pd.read_csv(uploaded_file)

        st.success(
            f"Dataset Loaded Successfully ({len(df)} rows)"
        )

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(),
            width="stretch"
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

        missing = [
            col for col in features
            if col not in df.columns
        ]

        if missing:

            st.error(
                f"Missing Columns: {missing}"
            )

            return

        if st.button("🚀 Generate Explanation"):

            with st.spinner(
                "Generating SHAP Explainability..."
            ):

                X = df[features].head(50)

                explainer = shap.TreeExplainer(
                    model
                )

                shap_values = explainer.shap_values(
                    X
                )

                st.success(
                    "SHAP Values Generated Successfully"
                )

                # =================================
                # FEATURE IMPORTANCE TABLE
                # =================================

                st.subheader(
                    "📊 Feature Importance Ranking"
                )

                importance = pd.DataFrame({

                    "Feature": X.columns,

                    "Importance":
                    np.abs(
                        shap_values
                    ).mean(axis=0)

                })

                importance = (
                    importance
                    .sort_values(
                        by="Importance",
                        ascending=False
                    )
                )

                st.dataframe(
                    importance,
                    width="stretch"
                )

                # =================================
                # BAR CHART
                # =================================

                st.subheader(
                    "📈 SHAP Feature Importance Chart"
                )

                st.bar_chart(
                    importance.set_index(
                        "Feature"
                    )
                )

                # =================================
                # SHAP SUMMARY PLOT
                # =================================

                st.subheader(
                    "🧠 SHAP Summary Plot"
                )

                fig = plt.figure(
                    figsize=(10, 6)
                )

                shap.summary_plot(
                    shap_values,
                    X,
                    plot_type="bar",
                    show=False
                )

                st.pyplot(
                    fig
                )

                plt.close()

                st.success(
                    "Explanation Generated Successfully"
                )

    except Exception as e:

        st.error(
            f"Explainability Error: {e}"
        )