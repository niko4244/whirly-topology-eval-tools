import argparse
import json
from critical_path import analyze_critical_path, visualize_critical_path
from power_analysis import estimate_power
from area_metrics import compute_area_metrics, generate_area_heatmap
from signal_integrity import analyze_signal_integrity
from fault_coverage import assess_fault_coverage

def load_topology(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    parser = argparse.ArgumentParser(description="Comprehensive VLSI Topology Evaluation Toolset")
    parser.add_argument('--input', type=str, required=True, help="Input topology JSON file")
    parser.add_argument('--output', type=str, default='reports', help="Output report directory")
    args = parser.parse_args()

    topology_data = load_topology(args.input)

    # Critical Path Analysis
    cp_results, cp_graph = analyze_critical_path(topology_data)
    visualize_critical_path(cp_graph, output_dir=args.output)

    # Power Analysis
    power_report = estimate_power(topology_data)

    # Area Metrics
    area_metrics = compute_area_metrics(topology_data)
    generate_area_heatmap(area_metrics, output_dir=args.output)

    # Signal Integrity
    si_report = analyze_signal_integrity(topology_data)

    # Fault Coverage
    fc_report = assess_fault_coverage(topology_data)

    # Aggregate and save reports
    aggregate_report = {
        "critical_path": cp_results,
        "power": power_report,
        "area": area_metrics,
        "signal_integrity": si_report,
        "fault_coverage": fc_report
    }
    with open(f"{args.output}/summary_report.json", "w") as f:
        json.dump(aggregate_report, f, indent=2)
    print(f"Reports generated in {args.output}/summary_report.json")

if __name__ == "__main__":
    main()