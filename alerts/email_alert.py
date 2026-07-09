import requests
import os


print("===== USING BREVO EMAIL API =====")


def send_alert_email(aqi, category, receiver_email):

    api_key = os.getenv("BREVO_API_KEY")

    if not api_key:
        raise Exception("BREVO_API_KEY not found.")

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Air Quality Prediction System",
            "email": "anshika.tiwari1829@gmail.com"
        },

        "to": [
            {
                "email": receiver_email
            }
        ],

        "subject": f"AQI Alert - {category}",

        "htmlContent": f"""
        <html>

        <body>

        <h2>🌍 Air Quality Alert</h2>

        <p><b>Predicted AQI:</b> {aqi}</p>

        <p><b>Category:</b> {category}</p>

        <p>Please take necessary precautions.</p>

        <hr>

        Air Quality Prediction and Monitoring System

        </body>

        </html>
        """
    }

    print("Sending Email via Brevo...")

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code in [200, 201]:

        print("EMAIL SENT SUCCESSFULLY")

        return response.json()

    raise Exception(response.text)