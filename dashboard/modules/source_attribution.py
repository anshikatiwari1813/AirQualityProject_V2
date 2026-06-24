import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt


def show_source_attribution():

    st.title("🏭 Pollution Source Attribution")

    st.markdown("""
    Analyze which pollutants contribute most
    to AQI predictions using SHAP Explainability.
    """)

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv"]
    )

    if uploaded_file is None:
        return

    # ==========================
    # LOAD DATASET
    # ==========================

    df = pd.read_csv(uploaded_file)

    # FAST MODE
    sample_size = st.slider(
        "Rows for Analysis",
        min_value=50,
        max_value=1000,
        value=300,
        step=50
    )

    if len(df) > sample_size:

        df = df.sample(
            n=sample_size,
            random_state=42
        )

    st.success(
        f"Using {len(df)} rows for analysis"
    )

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df.head(),
        width="stretch"
    )

    # ==========================
    # LOAD MODEL
    # ==========================

    try:

        model = joblib.load(
            "models/best_aqi_model.pkl"
        )

    except Exception as e:

        st.error(
            f"Model not found: {e}"
        )

        return

    # ==========================
    # SELECT NUMERIC FEATURES
    # ==========================

    feature_columns = []

    for col in df.columns:

        if col.upper() not in [
            "AQI",
            "CALCULATED_AQI"
        ]:

            if pd.api.types.is_numeric_dtype(
                df[col]
            ):

                feature_columns.append(col)

    if len(feature_columns) == 0:

        st.error(
            "No numeric features found."
        )

        return

    X = df[feature_columns]

    # SHAP FAST MODE

    if len(X) > 100:

        X = X.sample(
            100,
            random_state=42
        )

    # ==========================
    # SHAP ANALYSIS
    # ==========================

    with st.spinner(
        "Generating SHAP explanations..."
    ):

        explainer = shap.TreeExplainer(
            model
        )

        shap_values = explainer.shap_values(
            X
        )

    # ==========================
    # SHAP SUMMARY PLOT
    # ==========================

    st.subheader(
        "📊 SHAP Feature Importance"
    )

    fig = plt.figure(
        figsize=(10, 6)
    )

    shap.summary_plot(
        shap_values,
        X,
        show=False
    )

    st.pyplot(
        fig,
        clear_figure=True
    )

    # ==========================
    # FEATURE IMPORTANCE TABLE
    # ==========================

    importance = pd.DataFrame({

        "Feature": feature_columns,

        "Importance":
        abs(shap_values).mean(axis=0)

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    st.subheader(
        "🏆 Top Pollution Contributors"
    )

    st.dataframe(
        importance,
        width="stretch"
    )

    # ==========================
    # TOP 5 CONTRIBUTORS
    # ==========================

    st.subheader(
        "🔥 Top 5 AQI Drivers"
    )

    st.bar_chart(
        importance.head(5)
        .set_index("Feature")
    )

    # ==========================
    # INTERPRETATION
    # ==========================

    top_feature = (
        importance.iloc[0]["Feature"]
    )

    st.success(
        f"Most influential feature affecting AQI: {top_feature}"
    )

    st.info(
        """
        Higher SHAP importance means the feature
        contributes more strongly to AQI prediction.
        """
    )

    st.success(
        "✅ Source Attribution Analysis Complete"
    )