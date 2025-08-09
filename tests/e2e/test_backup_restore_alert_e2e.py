import os
from src.storage.s3_storage import S3Storage
from monitoring.slack_alerts import send_slack_alert

def test_backup_restore_and_alert(monkeypatch):
    s3 = S3Storage(os.environ['TEST_S3_BUCKET'])
    local_path = "/tmp/e2e_test.txt"
    restored_path = "/tmp/e2e_restored.txt"
    content = b"End-to-end test content"
    with open(local_path, "wb") as f:
        f.write(content)
    s3_key = "e2e/testfile.txt"
    s3.upload_file(local_path, s3_key)
    s3.download_file(s3_key, restored_path)
    with open(restored_path, "rb") as f:
        assert f.read() == content
    os.remove(local_path)
    os.remove(restored_path)

    called = {}
    def fake_post(url, json, timeout):
        called['url'] = url
        called['json'] = json
        class FakeResp:
            def raise_for_status(self): pass
        return FakeResp()
    monkeypatch.setattr("requests.post", fake_post)
    send_slack_alert("Backup and restore demo complete", "https://hooks.slack.com/services/test")
    assert called['json']['text'] == "Backup and restore demo complete"