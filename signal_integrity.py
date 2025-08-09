import numpy as np

def analyze_signal_integrity(topology_data):
    """
    Evaluates noise margin, crosstalk, timing violations, and process variation.

    Args:
        topology_data: dict with 'nets'

    Returns:
        si_report: dict per net
    """
    si_report = {}
    for net in topology_data.get('nets', []):
        noise_margin = net.get('noise_margin', 1.0)
        crosstalk = net.get('crosstalk', 0.0)
        delay_var = np.random.normal(0, 0.1)  # Placeholder for statistical delay
        severity_score = (crosstalk / max(noise_margin, 1e-3)) + abs(delay_var)
        si_report[net['id']] = {
            "noise_margin": noise_margin,
            "crosstalk": crosstalk,
            "stat_delay_var": delay_var,
            "severity_score": severity_score,
            "risk_flag": severity_score > 1.0
        }
    return si_report