import smtplib
from email.mime.text import MIMEText
import logging

def send_email_alert(subject, body, to_addr, from_addr="alerts@whirly.com", smtp_server="localhost"):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    try:
        with smtplib.SMTP(smtp_server) as server:
            server.sendmail(from_addr, [to_addr], msg.as_string())
        logging.info(f"Sent alert email to {to_addr}: {subject}")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

def alert_on_failure(event, user_email):
    subject = f"Whirly Alert: {event['type']} Failure"
    body = f"Dear User,\n\nA failure was detected: {event['details']}\n\nTimestamp: {event['timestamp']}"
    send_email_alert(subject, body, user_email)