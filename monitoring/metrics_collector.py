import requests

def collect_build_metrics():
    # Simulated build metrics
    return {"build_success_rate": 0.98, "average_test_time": 12.5, "flaky_tests": 2}

def report_metrics(metrics):
    print(f"Build Success Rate: {metrics['build_success_rate']*100:.1f}%")
    print(f"Avg Test Time: {metrics['average_test_time']}s")
    print(f"Flaky Tests: {metrics['flaky_tests']}")

if __name__ == "__main__":
    metrics = collect_build_metrics()
    report_metrics(metrics)