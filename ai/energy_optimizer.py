"""
Energy Optimization:
- Analyze appliance circuit usage patterns and utility rates.
- Recommend power-saving strategies and optimal operation times.
"""

import numpy as np

def recommend_usage_schedule(usage_profile, rate_schedule):
    """
    Suggest optimal appliance operation times for cost and grid impact reduction.
    Args:
        usage_profile (list of dict): [{'hour': int, 'expected_load': float}, ...]
        rate_schedule (dict): {hour: rate_per_kwh}
    Returns:
        list of dict: [{'hour': int, 'recommendation': str}]
    """
    recommendations = []
    for usage in usage_profile:
        hour = usage['hour']
        load = usage['expected_load']
        rate = rate_schedule.get(hour, 0.25)  # default rate if not specified
        if rate < 0.15 and load > 0.5:
            recommendations.append({
                'hour': hour,
                'recommendation': 'Run appliance (low cost, low grid impact)'
            })
        elif rate > 0.25 and load > 0.5:
            recommendations.append({
                'hour': hour,
                'recommendation': 'Avoid use (high cost period)'
            })
        else:
            recommendations.append({
                'hour': hour,
                'recommendation': 'OK to use'
            })
    return recommendations

def analyze_usage_patterns(sensor_data):
    """
    Analyze historical circuit data for power-saving strategy suggestions.
    Args:
        sensor_data (list of dict): [{'timestamp': str, 'current': float, 'voltage': float}, ...]
    Returns:
        dict: { 'average_power': float, 'peak_hours': list }
    """
    powers = [d['current'] * d['voltage'] for d in sensor_data]
    timestamps = [d['timestamp'] for d in sensor_data]
    avg_power = np.mean(powers)
    # Simple peak hours detection (could be improved with more data)
    hour_counts = {}
    for ts in timestamps:
        hour = int(ts.split("T")[1].split(":")[0])
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    peak_hours = sorted(hour_counts, key=hour_counts.get, reverse=True)[:3]
    return {
        'average_power': avg_power,
        'peak_hours': peak_hours
    }