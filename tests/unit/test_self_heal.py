import pytest
from monitoring.self_heal import restart_service, monitor_and_self_heal

def test_restart_service(monkeypatch):
    called = {}
    def fake_run(cmd, check):
        called['cmd'] = cmd
        called['check'] = check
    monkeypatch.setattr("subprocess.run", fake_run)
    restart_service("test-service")
    assert called['cmd'] == ["systemctl", "restart", "test-service"]
    assert called['check'] is True

def test_monitor_and_self_heal(monkeypatch):
    events = {"restarted": False, "checks": 0}
    def fake_health():
        events["checks"] += 1
        return events["checks"] < 2
    def fake_restart(service):
        events["restarted"] = True
    monkeypatch.setattr("monitoring.self_heal.restart_service", fake_restart)
    # Run just a couple of loops
    import threading
    def run_monitor():
        monitor_and_self_heal(fake_health, "test-service", interval=0.01)
    t = threading.Thread(target=run_monitor, daemon=True)
    t.start()
    time.sleep(0.05)
    assert events["restarted"] is True