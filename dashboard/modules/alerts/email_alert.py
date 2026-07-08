import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_alert_email(aqi, category, receiver_email):

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    sender_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not sender_email:
        raise Exception("SMTP_EMAIL not found")

    if not smtp_password:
        raise Exception("SMTP_PASSWORD not found")

    subject = f"🌍 AQI Alert - {category}"

    html = f"""
    <html>

    <body>

    <h2>🌍 Air Quality Alert</h2>

    <p><b>Predicted AQI:</b> {aqi}</p>

    <p><b>Category:</b> {category}</p>

    <hr>

    <p>
    This email was generated automatically by
    Air Quality Prediction & Monitoring System.
    </p>

    </body>

    </html>
    """

    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(
        MIMEText(html, "html")
    )

    try:

        print("========== BREVO SMTP ==========")
        print("Connecting...")

        server = smtplib.SMTP(
            smtp_server,
            smtp_port
        )

        server.starttls()

        print("Logging in...")

        server.login(
            sender_email,
            smtp_password
        )

        print("Sending...")

        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )

        server.quit()

        print("EMAIL SENT SUCCESSFULLY")

        return {
            "status": "success"
        }

    except Exception as e:

        print("SMTP ERROR:", str(e))

        raise Exception(str(e))