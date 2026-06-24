import streamlit as st
import sqlite3
import pandas as pd


def show_database_analytics():

    st.title("📊 Database Analytics Dashboard")

    conn = sqlite3.connect(
        "air_quality.db"
    )

    df = pd.read_sql(
        "SELECT * FROM predictions",
        conn
    )

    conn.close()

    if df.empty:

        st.warning(
            "No prediction data available."
        )

        return

    st.success(
        f"Total Records: {len(df)}"
    )

    # ==========================
    # KPI CARDS
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Predictions",
            len(df)
        )

    with col2:

        st.metric(
            "Average AQI",
            round(
                df["predicted_aqi"].mean(),
                2
            )
        )

    with col3:

        st.metric(
            "Maximum AQI",
            round(
                df["predicted_aqi"].max(),
                2
            )
        )

    with col4:

        st.metric(
            "Minimum AQI",
            round(
                df["predicted_aqi"].min(),
                2
            )
        )

    st.markdown("---")

    # ==========================
    # AQI TREND
    # ==========================

    st.subheader("📈 AQI Trend")

    trend_df = df.sort_values(
        by="id"
    )

    st.line_chart(
        trend_df["predicted_aqi"]
    )

    st.markdown("---")

    # ==========================
    # CATEGORY DISTRIBUTION
    # ==========================

    st.subheader("🥧 AQI Category Distribution")

    category_counts = (
        df["category"]
        .value_counts()
    )

    st.bar_chart(
        category_counts
    )

    st.markdown("---")

    # ==========================
    # POLLUTANT ANALYSIS
    # ==========================

    st.subheader("🌫 Average Pollutant Levels")

    pollutant_df = pd.DataFrame({

        "PM2.5":
            [df["pm25"].mean()],

        "PM10":
            [df["pm10"].mean()],

        "NO2":
            [df["no2"].mean()],

        "SO2":
            [df["so2"].mean()],

        "CO":
            [df["co"].mean()],

        "O3":
            [df["o3"].mean()]
    })

    st.bar_chart(
        pollutant_df.T
    )

    st.markdown("---")

    # ==========================
    # RECENT PREDICTIONS
    # ==========================

    st.subheader("🕒 Latest Predictions")

    st.dataframe(
        df.sort_values(
            by="id",
            ascending=False
        ).head(10),
        width="stretch"
    )

    st.markdown("---")

    # ==========================
    # DOWNLOAD
    # ==========================

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "⬇ Download Analytics Data",
        csv,
        "database_analytics.csv",
        "text/csv"
    )