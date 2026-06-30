import streamlit as st
import pandas as pd

from sqlalchemy import text
from database.postgres_db import engine


def show_prediction_history():

    st.title("📜 Prediction History")

    with engine.connect() as conn:

        df = pd.read_sql(
            text("""
            SELECT *
            FROM predictions
            ORDER BY id DESC
            """),
            conn
        )

    if df.empty:

        st.warning(
            "No prediction history found."
        )

        return

    st.success(
        f"Total Predictions: {len(df)}"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("📈 AQI Trend")

    st.line_chart(
        df["predicted_aqi"]
    )

    st.subheader("📊 Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average AQI",
            round(
                df["predicted_aqi"].mean(),
                2
            )
        )

    with col2:

        st.metric(
            "Maximum AQI",
            round(
                df["predicted_aqi"].max(),
                2
            )
        )

    with col3:

        st.metric(
            "Minimum AQI",
            round(
                df["predicted_aqi"].min(),
                2
            )
        )

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "⬇ Download CSV",
        csv,
        "prediction_history.csv",
        "text/csv"
    )