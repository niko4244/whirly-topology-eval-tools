import pytest

def test_addition():
    assert 1 + 1 == 2

def test_mocking(monkeypatch):
    class Dummy:
        def value(self):
            return 42
    d = Dummy()
    monkeypatch.setattr(Dummy, "value", lambda self: 99)
    assert d.value() == 99