import os
from src.storage.s3_storage import S3Storage
from monitoring.slack_alerts import send_slack_alert
from monitoring.self_heal import monitor_and_self_heal

def test_full_appliance_monitoring(monkeypatch):
    # Setup S3 mock
    s3 = S3Storage(os.environ['TEST_S3_BUCKET'])
    test_file = "/tmp/lifecycle_test.txt"
    with open(test_file, "wb") as f:
        f.write(b"appliance status snapshot")
    s3_key = "e2e/lifecycle.txt"
    s3.upload_file(test_file, s3_key)
    s3.download_file(s3_key, test_file + ".restored")
    assert open(test_file + ".restored", "rb").read() == b"appliance status snapshot"
    os.remove(test_file)
    os.remove(test_file + ".restored")

    # Simulate alert integration
    called = {}
    def fake_post(url, json, timeout):
        called['url'] = url
        called['json'] = json
        class FakeResp:
            def raise_for_status(self): pass
        return FakeResp()
    monkeypatch.setattr("requests.post", fake_post)
    send_slack_alert("Appliance fault detected", "https://hooks.slack.com/services/test")
    assert "fault" in called['json']['text']

    # Self-healing simulation
    restart_events = []
    def fake_restart(service):
        restart_events.append(service)
    monkeypatch.setattr("monitoring.self_heal.restart_service", fake_restart)
    def health_check(): return False
    monitor_and_self_heal(health_check, "demo-appliance", interval=0.01)
    assert "demo-appliance" in restart_events