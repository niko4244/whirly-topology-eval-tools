# Webhook & Slack Alerts

## Overview

- `monitoring/slack_alerts.py`: Send formatted alerts to Slack via webhook.
- `monitoring/webhook_alerts.py`: Send generic event notifications to any webhook endpoint.

## Usage

### Send Slack Alert

```python
from monitoring.slack_alerts import send_slack_alert
send_slack_alert("Backup failed!", "https://hooks.slack.com/services/your/webhook/url")
```

### Send Webhook Alert

```python
from monitoring.webhook_alerts import send_webhook_alert
send_webhook_alert("incident", {"info": "failure"}, "http://webhook.test/alert")
```

## Testing

Unit tests provided:
- `tests/unit/test_slack_alerts.py`
- `tests/unit/test_webhook_alerts.py`

## Notes

- Slack/webhook URLs must be provided as secrets/env variables.
- Alerts should be triggered on backup failures, unhealthy metrics, and security events.