import streamlit as st

# =====================================
# AQI CATEGORY
# =====================================

def get_aqi_category(aqi):

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


# =====================================
# HEALTH ADVISORY
# =====================================

def get_health_advisory(aqi):

    if aqi <= 50:
        return """
✅ Air quality is excellent.

• Safe for outdoor activities
• Safe for children and elderly
• No health risk
"""

    elif aqi <= 100:
        return """
🟡 Air quality is acceptable.

• Normal outdoor activities allowed
• Sensitive individuals should monitor symptoms
"""

    elif aqi <= 200:
        return """
🟠 Moderate pollution.

• Children and elderly should limit outdoor activities
• Asthma patients should be careful
• Wear mask if exposed for long periods
"""

    elif aqi <= 300:
        return """
🔴 Poor Air Quality.

• Avoid prolonged outdoor activities
• Wear N95 mask outdoors
• Keep windows closed
"""

    elif aqi <= 400:
        return """
🟣 Very Poor Air Quality.

• Stay indoors whenever possible
• Avoid exercise outdoors
• Use air purifier if available
"""

    else:
        return """
⚫ Severe Air Quality.

• Health emergency conditions
• Stay indoors
• Use N95/N99 mask
• Avoid all unnecessary travel
• Seek medical attention if breathing issues occur
"""


# =====================================
# MAIN PAGE
# =====================================

def show_health():

    st.title("🏥 Health Advisory System")

    st.markdown(
        """
        Get personalized health recommendations
        based on AQI level.
        """
    )

    aqi = st.slider(
        "Select AQI Value",
        0,
        500,
        100
    )

    category = get_aqi_category(aqi)

    st.metric(
        "AQI Category",
        category
    )

    st.subheader("Health Recommendations")

    st.info(
        get_health_advisory(aqi)
    )

    st.subheader("Sensitive Groups")

    if aqi > 100:

        st.warning(
            """
⚠ High Risk Groups:

• Children
• Elderly People
• Asthma Patients
• Heart Disease Patients
• Pregnant Women
"""
        )

    st.subheader("AQI Scale")

    st.progress(aqi / 500)

    st.write(
        f"Current AQI Level: {aqi}"
    )