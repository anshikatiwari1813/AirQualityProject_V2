import streamlit as st
from alerts.email_alert import send_alert_email


def show_alert_center():

    st.title("📧 AQI Alert Center")

    st.markdown(
        "Send AQI alerts directly from dashboard."
    )

    email = st.text_input(
        "Receiver Email"
    )

    threshold = st.slider(
        "AQI Alert Threshold",
        50,
        500,
        200
    )

    st.info(
        f"Alert will trigger when AQI exceeds {threshold}"
    )

    st.markdown("---")

    test_aqi = st.number_input(
        "Test AQI",
        value=250
    )

    category = st.text_input(
        "Category",
        value="Poor 🔴"
    )

    if st.button("📨 Send Test Alert"):

        if email == "":

            st.error(
                "Enter email address first."
            )

        else:

            try:

                send_alert_email(
                    test_aqi,
                    category,
                    email
                )

                st.success(
                    "Alert Email Sent Successfully!"
                )

            except Exception as e:

                st.error(
                    str(e)
                )