import requests
import logging

def send_slack_alert(message, webhook_url):
    payload = {"text": message}
    try:
        resp = requests.post(webhook_url, json=payload, timeout=5)
        resp.raise_for_status()
        logging.info(f"Slack alert sent: {message}")
    except Exception as e:
        logging.error(f"Failed to send slack alert: {e}")

def alert_on_security_event(event, webhook_url):
    msg = f"*Security Alert*: {event['type']}\nDetails: {event['details']}\nTimestamp: {event['timestamp']}"
    send_slack_alert(msg, webhook_url)