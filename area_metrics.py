import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def compute_area_metrics(topology_data):
    """
    Computes placement density, congestion, and violations for each block.

    Args:
        topology_data: dict with 'blocks', each with 'components'

    Returns:
        metrics: list of dicts per block
    """
    metrics = []
    for block in topology_data.get('blocks', []):
        area = sum([comp.get('area', 0) for comp in block.get('components', [])])
        density = area / block.get('block_area', 1)
        violations = sum([comp.get('spacing_violation', 0) for comp in block.get('components', [])])
        congestion = block.get('routing_congestion', 0)
        metrics.append({
            "block_id": block['id'],
            "area": area,
            "density": density,
            "spacing_violations": violations,
            "routing_congestion": congestion
        })
    return metrics

def generate_area_heatmap(metrics, output_dir='reports'):
    """
    Generates a heatmap (PNG) of block densities.

    Args:
        metrics: list of dicts from compute_area_metrics
        output_dir: where to save
    """
    data = np.array([m['density'] for m in metrics]).reshape(1, -1)
    plt.figure(figsize=(8,2))
    sns.heatmap(data, cmap="YlOrRd", annot=True)
    plt.title("Placement Density Heatmap")
    plt.savefig(f"{output_dir}/area_density_heatmap.png")
    plt.close()