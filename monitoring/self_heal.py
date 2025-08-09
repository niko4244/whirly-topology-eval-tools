import subprocess
import time
import logging

def restart_service(service_name):
    try:
        subprocess.run(["systemctl", "restart", service_name], check=True)
        logging.info(f"Restarted service: {service_name}")
    except Exception as e:
        logging.error(f"Failed to restart {service_name}: {e}")

def monitor_and_self_heal(health_check_func, service_name, interval=60):
    while True:
        healthy = health_check_func()
        if not healthy:
            logging.warning(f"Service {service_name} unhealthy. Attempting restart...")
            restart_service(service_name)
        time.sleep(interval)

# Example usage:
# monitor_and_self_heal(check_backend_health, "whirly-backend")