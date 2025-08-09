"""
IoT & Cloud Integration:
- Securely stream appliance data to the cloud for remote diagnostics, analytics, and upgrades.
- Support for MQTT, WebSockets, or RESTful integration.
- Enable remote viewing and troubleshooting by users or technicians.
"""

import ssl
import json
import paho.mqtt.client as mqtt

class IoTGateway:
    def __init__(self, mqtt_host, mqtt_port, username=None, password=None, ca_cert=None):
        self.client = mqtt.Client()
        if username and password:
            self.client.username_pw_set(username, password)
        if ca_cert:
            self.client.tls_set(ca_cert, tls_version=ssl.PROTOCOL_TLS)
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port

    def connect(self):
        self.client.connect(self.mqtt_host, self.mqtt_port)
        self.client.loop_start()

    def stream_data_to_cloud(self, appliance_id, data):
        """
        Publishes appliance data to the cloud.
        Args:
            appliance_id (str): Unique identifier for the appliance.
            data (dict): Sensor or status data.
        Returns:
            bool: Success status.
        """
        topic = f"appliance/{appliance_id}/data"
        payload = json.dumps(data)
        result = self.client.publish(topic, payload)
        return result.rc == mqtt.MQTT_ERR_SUCCESS

    def remote_diagnostics(self, appliance_id):
        """
        Requests and retrieves remote diagnostics data.
        Args:
            appliance_id (str): Unique identifier for the appliance.
        Returns:
            dict: Diagnostic data (simulate for now).
        """
        # In a real implementation, this would subscribe and receive real-time diagnostics.
        # Here, simulate a cloud query:
        return {
            "appliance_id": appliance_id,
            "diagnostics": {
                "last_checked": "2025-08-09T03:58:21Z",
                "status": "healthy",
                "faults": []
            }
        }

# Example usage:
if __name__ == "__main__":
    gateway = IoTGateway(
        mqtt_host="broker.example.com",
        mqtt_port=8883,
        username="iotuser",
        password="iotpass",
        ca_cert="path/to/ca.crt"
    )
    gateway.connect()
    status = gateway.stream_data_to_cloud("dryer-001", {"temp": 42, "current": 3.5, "status": "normal"})
    print("Data stream successful:", status)
    diagnostics = gateway.remote_diagnostics("dryer-001")
    print(diagnostics)