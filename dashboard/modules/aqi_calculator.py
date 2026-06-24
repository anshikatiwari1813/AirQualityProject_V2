import streamlit as st

# ==========================================
# AQI CATEGORY
# ==========================================

def get_category(aqi):

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


# ==========================================
# HEALTH ADVISORY
# ==========================================

def get_health_advice(aqi):

    if aqi <= 50:
        return "Air quality is excellent. Enjoy outdoor activities."

    elif aqi <= 100:
        return "Air quality is acceptable for most people."

    elif aqi <= 200:
        return "Sensitive individuals should limit outdoor exposure."

    elif aqi <= 300:
        return "Avoid prolonged outdoor activities."

    elif aqi <= 400:
        return "Stay indoors whenever possible."

    else:
        return "Health emergency conditions. Avoid going outside."


# ==========================================
# AQI CALCULATOR PAGE
# ==========================================

def show_aqi_calculator():

    st.title("🧮 AQI Calculator")

    st.markdown(
        """
        Calculate Air Quality Index using pollutant concentrations.
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        pm25 = st.number_input(
            "PM2.5 (µg/m³)",
            min_value=0.0,
            value=80.0
        )

        pm10 = st.number_input(
            "PM10 (µg/m³)",
            min_value=0.0,
            value=150.0
        )

        no2 = st.number_input(
            "NO₂ (µg/m³)",
            min_value=0.0,
            value=40.0
        )

    with col2:

        so2 = st.number_input(
            "SO₂ (µg/m³)",
            min_value=0.0,
            value=20.0
        )

        co = st.number_input(
            "CO (mg/m³)",
            min_value=0.0,
            value=1.0
        )

        o3 = st.number_input(
            "O₃ (µg/m³)",
            min_value=0.0,
            value=35.0
        )

    if st.button("🚀 Calculate AQI"):

        # Simple AQI Approximation
        aqi = max(
            pm25 * 2,
            pm10 * 0.8,
            no2 * 1.2,
            so2 * 1.1,
            co * 40,
            o3 * 1.0
        )

        category = get_category(aqi)

        st.success(
            f"Calculated AQI : {aqi:.2f}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "AQI Value",
                round(aqi, 2)
            )

        with col2:

            st.metric(
                "AQI Category",
                category
            )

        st.warning(
            get_health_advice(aqi)
        )

        st.subheader("📊 AQI Meter")

        st.progress(
            min(int(aqi), 500) / 500
        )

        st.subheader("📋 Input Summary")

        st.dataframe(
            {
                "Pollutant": [
                    "PM2.5",
                    "PM10",
                    "NO₂",
                    "SO₂",
                    "CO",
                    "O₃"
                ],
                "Value": [
                    pm25,
                    pm10,
                    no2,
                    so2,
                    co,
                    o3
                ]
            },
            use_container_width=True
        )

        st.subheader("🌫 AQI Categories")

        st.info(
            """
            0-50      → Good 🟢

            51-100    → Satisfactory 🟡

            101-200   → Moderate 🟠

            201-300   → Poor 🔴

            301-400   → Very Poor 🟣

            401-500   → Severe ⚫
            """
        )
