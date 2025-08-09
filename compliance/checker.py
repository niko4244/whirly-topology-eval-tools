"""
Safety Compliance Checking:
- Scan appliance circuit maps for electrical code compliance.
- Generate official compliance reports/certificates for insurance or regulatory use.
"""

import datetime
import json

def scan_for_code_compliance(circuit_map, standards=None):
    """
    Analyze a circuit map for safety compliance.
    Args:
        circuit_map (dict): { 'nodes': [...], 'connections': [...], 'ratings': {...} }
        standards (list of str): List of codes/standards to check (e.g., ['NEC', 'IEC'])
    Returns:
        dict: { 'compliant': bool, 'issues': [str], 'checked_standards': list }
    """
    issues = []
    checked = standards or ['NEC', 'IEC']
    # Example checks (expand with real logic per standard):
    for node in circuit_map.get('nodes', []):
        rating = circuit_map.get('ratings', {}).get(node)
        if not rating:
            issues.append(f"{node}: No rating info.")
        elif rating < 5:  # Arbitrary threshold for demo
            issues.append(f"{node}: Rating too low for standard operation.")
    for conn in circuit_map.get('connections', []):
        if conn[0] == conn[1]:
            issues.append(f"Invalid connection: {conn[0]} connected to itself.")
    compliant = len(issues) == 0
    return {
        'compliant': compliant,
        'issues': issues,
        'checked_standards': checked
    }

def generate_compliance_report(appliance_id, circuit_map, scan_result, output_path=None):
    """
    Generate a compliance report in JSON or PDF format.
    Args:
        appliance_id (str): Unique identifier for the appliance.
        circuit_map (dict): The device's circuit map.
        scan_result (dict): Compliance scan results.
        output_path (str): File path to save report (JSON).
    Returns:
        str: Path to generated report.
    """
    report = {
        'appliance_id': appliance_id,
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'circuit_map': circuit_map,
        'compliance': scan_result
    }
    if output_path is None:
        output_path = f"{appliance_id}_compliance_report.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    # TODO: Optionally export to PDF for formal certificates using a library like reportlab.
    return output_path