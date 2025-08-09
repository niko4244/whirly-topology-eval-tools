"""
Security Monitoring:
- Detect suspicious or unauthorized activity (e.g., abnormal power draw, firmware tampering).
- Alert users and lock down unsafe or compromised appliances.
"""

import datetime

def detect_suspicious_activity(sensor_data, firmware_version, allowed_versions, power_threshold=100.0):
    """
    Analyze sensor and firmware data for security anomalies.
    Args:
        sensor_data (dict): { 'appliance_id': str, 'current': float, 'voltage': float, 'timestamp': str }
        firmware_version (str): Current firmware version.
        allowed_versions (list of str): List of approved firmware versions.
        power_threshold (float): Maximum allowed power before flagging.
    Returns:
        dict: { 'suspicious': bool, 'reasons': [str] }
    """
    reasons = []
    power = sensor_data['current'] * sensor_data['voltage']
    if power > power_threshold:
        reasons.append(f"Abnormal power draw: {power}W exceeds threshold.")
    if firmware_version not in allowed_versions:
        reasons.append(f"Firmware version {firmware_version} is not authorized.")
    suspicious = len(reasons) > 0
    return {
        'suspicious': suspicious,
        'reasons': reasons,
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'appliance_id': sensor_data.get('appliance_id')
    }

def lock_down_appliance(appliance_id):
    """
    Remotely disable or isolate an unsafe appliance.
    Args:
        appliance_id (str): Unique identifier for the appliance.
    Returns:
        str: Status message.
    """
    # TODO: Implement remote disable logic via device API, relay, etc.
    timestamp = datetime.datetime.utcnow().isoformat()
    return f"Appliance {appliance_id} locked down at {timestamp} due to security concerns."