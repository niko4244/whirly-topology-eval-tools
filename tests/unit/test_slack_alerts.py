import pytest
from monitoring.slack_alerts import send_slack_alert

def test_send_slack_alert(monkeypatch):
    called = {}
    def fake_post(url, json, timeout):
        called['url'] = url
        called['json'] = json
        class FakeResp:
            def raise_for_status(self): pass
        return FakeResp()
    monkeypatch.setattr("requests.post", fake_post)
    send_slack_alert("Hello!", "https://hooks.slack.com/services/test")
    assert called['url'] == "https://hooks.slack.com/services/test"
    assert called['json']['text'] == "Hello!"
