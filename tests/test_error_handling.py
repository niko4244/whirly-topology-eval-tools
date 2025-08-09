from core.error_handling import error_wrapper, setup_logging

def test_error_wrapper_logs_and_raises(tmp_path):
    setup_logging(str(tmp_path / "test.log"))
    @error_wrapper
    def fail_func():
        raise ValueError("Test error")
    try:
        fail_func()
    except ValueError as e:
        assert "Test error" in str(e)