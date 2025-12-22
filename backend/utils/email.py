import smtplib
from email.message import EmailMessage
from config.settings import settings

def send_secret_key_email(to_email: str, secret_key: str):
    msg = EmailMessage()
    msg["Subject"] = "Your Secret Chat Key 🔐"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email

    msg.set_content(f"""
Your secret chat room has been created.

🔑 Secret Key:
{secret_key}

⚠️ Do not share this key with anyone.
""")

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.send_message(msg)
