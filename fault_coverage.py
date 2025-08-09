def assess_fault_coverage(topology_data):
    """
    Assesses fault coverage for each block using standard fault models.

    Args:
        topology_data: dict with 'blocks', each with 'faults'

    Returns:
        fc_report: dict per block + overall summary
    """
    fc_report = {}
    total_faults = 0
    detected_faults = 0
    for block in topology_data.get('blocks', []):
        faults = block.get('faults', {})
        block_faults = faults.get('total', 100)
        block_detected = faults.get('detected', 80)
        block_stuck_at = faults.get('stuck_at', 50)
        block_transition = faults.get('transition', 20)
        block_path_delay = faults.get('path_delay', 10)
        coverage_pct = (block_detected / block_faults) * 100 if block_faults else 0
        recommendations = []
        if coverage_pct < 95:
            recommendations.append("Increase test pattern count or diversify fault models.")
        fc_report[block['id']] = {
            "total_faults": block_faults,
            "detected_faults": block_detected,
            "coverage_pct": coverage_pct,
            "stuck_at_faults": block_stuck_at,
            "transition_faults": block_transition,
            "path_delay_faults": block_path_delay,
            "recommendations": recommendations
        }
        total_faults += block_faults
        detected_faults += block_detected
    fc_report["overall_coverage"] = {
        "total_faults": total_faults,
        "detected_faults": detected_faults,
        "coverage_pct": (detected_faults / total_faults) * 100 if total_faults else 0
    }
    return fc_report