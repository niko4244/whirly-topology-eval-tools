import numpy as np

def estimate_power(topology_data, mode='typical'):
    """
    Estimates static and dynamic power consumption for each block/component.

    Args:
        topology_data: dict with 'blocks', each containing 'components' with leakage/switching
        mode: 'worst', 'typical', 'best'

    Returns:
        report: dict with hierarchical breakdown
    """
    static_power = 0.0
    dynamic_power = 0.0
    block_reports = {}
    scaling = {'worst': 1.2, 'typical': 1.0, 'best': 0.8}.get(mode, 1.0)
    for block in topology_data.get('blocks', []):
        leakage = np.sum([comp.get('leakage', 0) for comp in block.get('components', [])]) * scaling
        switching = np.sum([comp.get('switching', 0) for comp in block.get('components', [])]) * scaling
        block_reports[block['id']] = {
            "static_power": leakage,
            "dynamic_power": switching,
            "total_power": leakage + switching
        }
        static_power += leakage
        dynamic_power += switching
    report = {
        "mode": mode,
        "static_power": static_power,
        "dynamic_power": dynamic_power,
        "total_power": static_power + dynamic_power,
        "block_level": block_reports
    }
    return report