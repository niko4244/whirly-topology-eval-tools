import os
from src.storage.s3_storage import S3Storage
from monitoring.slack_alerts import send_slack_alert

def demo_backup_and_alert():
    s3 = S3Storage(bucket_name=os.environ["DEMO_S3_BUCKET"])
    file_path = "/tmp/demo_file.txt"
    s3_key = "demo/demo_file.txt"
    with open(file_path, "w") as f:
        f.write("Demo backup content")
    s3.upload_file(file_path, s3_key)
    alert_url = os.environ.get("DEMO_SLACK_WEBHOOK")
    if alert_url:
        send_slack_alert(f"Backup completed for {s3_key}", alert_url)
    os.remove(file_path)
    print("Demo backup and alert completed.")

if __name__ == "__main__":
    demo_backup_and_alert()