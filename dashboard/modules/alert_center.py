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
        min_value=0,
        max_value=500,
        value=250
    )

    category = st.text_input(
        "Category",
        value="Poor 🔴"
    )

    if st.button("📨 Send Test Alert"):

        st.write("BUTTON CLICKED")

        print("BUTTON CLICKED")

        if not email:

            st.error(
                "Please enter receiver email."
            )

        else:

            try:

                print("CALLING send_alert_email()")

                result = send_alert_email(
                    test_aqi,
                    category,
                    email
                )

                print("FUNCTION COMPLETED")

                st.success(
                    f"✅ Alert Email Sent Successfully to {email}"
                )

                st.write(
                    "Response:",
                    result
                )

            except Exception as e:

                print("ERROR:", str(e))

                st.error(
                    f"❌ Email Sending Failed: {str(e)}"
                )