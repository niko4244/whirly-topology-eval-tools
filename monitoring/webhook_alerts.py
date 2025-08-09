import requests
import logging

def send_webhook_alert(event_type, details, webhook_url):
    payload = {
        "event_type": event_type,
        "details": details
    }
    try:
        resp = requests.post(webhook_url, json=payload, timeout=5)
        resp.raise_for_status()
        logging.info(f"Webhook alert sent: {event_type}")
    except Exception as e:
        logging.error(f"Failed to send webhook alert: {e}")

def alert_on_incident(event, webhook_url):
    send_webhook_alert(event['type'], event['details'], webhook_url)