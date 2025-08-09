import os
import time
from src.storage.s3_storage import S3Storage
from monitoring.slack_alerts import send_slack_alert
from monitoring.prometheus_metrics import setup_metrics, ACTIVE_USERS, FAILED_REQUESTS
from monitoring.self_heal import restart_service

def interactive_demo():
    setup_metrics(port=8003)
    s3 = S3Storage(bucket_name=os.environ["DEMO_S3_BUCKET"])
    print("Welcome to Smart Circuit Analyzer Demo.")
    appliance = input("Enter appliance name (e.g., dryer): ")
    status = input("Enter status (healthy/faulty): ").strip().lower()
    ACTIVE_USERS.inc()
    file_path = f"/tmp/{appliance}_demo.txt"
    with open(file_path, "w") as f:
        f.write(f"{appliance} status: {status}")
    s3_key = f"demo/{appliance}_status.txt"
    s3.upload_file(file_path, s3_key)
    print(f"Status snapshot for {appliance} uploaded to S3.")

    if status == "faulty":
        FAILED_REQUESTS.inc()
        alert_url = os.environ.get("DEMO_SLACK_WEBHOOK")
        if alert_url:
            send_slack_alert(f"Fault detected in {appliance}. Initiating self-heal.", alert_url)
        print("Self-healing initiated...")
        restart_service(appliance)
        print(f"{appliance} restarted.")
    else:
        print(f"{appliance} is healthy. No action needed.")
    os.remove(file_path)

if __name__ == "__main__":
    interactive_demo()