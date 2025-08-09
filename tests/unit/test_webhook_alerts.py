import pytest
from monitoring.webhook_alerts import send_webhook_alert

def test_send_webhook_alert(monkeypatch):
    called = {}
    def fake_post(url, json, timeout):
        called['url'] = url
        called['json'] = json
        class FakeResp:
            def raise_for_status(self): pass
        return FakeResp()
    monkeypatch.setattr("requests.post", fake_post)
    send_webhook_alert("incident", {"info": "failure"}, "http://webhook.test/alert")
    assert called['url'] == "http://webhook.test/alert"
    assert called['json']['event_type'] == "incident"
    assert called['json']['details']['info'] == "failure"