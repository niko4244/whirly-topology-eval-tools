"""
Automated Documentation & Learning:
- Auto-generate wiring diagrams and circuit maps from live analysis.
- Maintain searchable maintenance logs and knowledge base for appliances, faults, and fixes.
"""

import datetime
import json

def generate_wiring_diagram(appliance_config, output_path):
    """
    Generate a wiring diagram (Graphviz DOT format) from appliance circuit configuration.
    Args:
        appliance_config (dict): { 'nodes': [...], 'connections': [...] }
        output_path (str): File path to save diagram.
    Returns:
        output_path (str): Path to generated diagram.
    """
    # Example: nodes = ["Fuse", "Relay", "Motor"], connections = [("Fuse", "Relay"), ("Relay", "Motor")]
    dot = "digraph G {\n"
    for node in appliance_config.get("nodes", []):
        dot += f'    "{node}";\n'
    for conn in appliance_config.get("connections", []):
        a, b = conn
        dot += f'    "{a}" -> "{b}";\n'
    dot += "}\n"
    with open(output_path, "w") as f:
        f.write(dot)
    return output_path

def log_maintenance_event(appliance_id, event_type, detail, log_path="maintenance_log.json"):
    """
    Log a maintenance event to the appliance's history.
    Args:
        appliance_id (str): Unique appliance identifier.
        event_type (str): Event type (e.g., 'repair', 'diagnosis', 'upgrade').
        detail (str): Description/details of event.
        log_path (str): Path to log file.
    Returns:
        None
    """
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "appliance_id": appliance_id,
        "event_type": event_type,
        "detail": detail
    }
    try:
        with open(log_path, "r") as f:
            log = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        log = []
    log.append(entry)
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

def search_knowledge_base(query, log_path="maintenance_log.json"):
    """
    Search the maintenance log knowledge base for matching events.
    Args:
        query (str): Search string.
        log_path (str): Path to log file.
    Returns:
        list: Matching entries.
    """
    try:
        with open(log_path, "r") as f:
            log = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []
    return [entry for entry in log if query.lower() in entry["detail"].lower()]