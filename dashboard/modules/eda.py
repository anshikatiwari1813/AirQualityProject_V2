import streamlit as st

def show_eda():

    st.title("📊 EDA Dashboard")

    st.subheader("AQI Distribution")

    try:
        st.image("outputs/aqi_distribution.png")
    except:
        st.warning("AQI Distribution Image Not Found")

    st.subheader("Correlation Heatmap")

    try:
        st.image("outputs/correlation_heatmap.png")
    except:
        st.warning("Heatmap Not Found")