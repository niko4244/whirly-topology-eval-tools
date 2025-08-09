import networkx as nx
import matplotlib.pyplot as plt

def analyze_critical_path(topology_data):
    """
    Identifies the critical path (longest delay) in the circuit topology.

    Args:
        topology_data: dict containing 'nodes' and 'edges'. Each edge should have a 'delay' value.

    Returns:
        results: dict with path and total delay
        G: networkx.DiGraph for visualization
    """
    G = nx.DiGraph()
    for node in topology_data.get('nodes', []):
        G.add_node(node['id'], **node)
    for edge in topology_data.get('edges', []):
        G.add_edge(edge['source'], edge['target'], delay=edge.get('delay', 1.0))
    cp = nx.dag_longest_path(G, weight='delay')
    cp_length = nx.dag_longest_path_length(G, weight='delay')
    results = {
        "critical_path": cp,
        "critical_path_length": cp_length
    }
    return results, G

def visualize_critical_path(G, output_dir='reports'):
    """
    Saves a visualization highlighting the critical path.

    Args:
        G: networkx.DiGraph
        output_dir: where to save the PNG
    """
    cp = nx.dag_longest_path(G, weight='delay')
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10,7))
    nx.draw(G, pos, with_labels=True, node_color='lightgrey', edge_color='grey')
    cp_edges = list(zip(cp[:-1], cp[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=cp, node_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=cp_edges, edge_color='red', width=2)
    plt.title("Critical Path Visualization")
    plt.savefig(f"{output_dir}/critical_path.png")
    plt.close()