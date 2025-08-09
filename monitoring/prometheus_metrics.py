from prometheus_client import start_http_server, Summary, Counter, Gauge

REQUEST_TIME = Summary("whirly_request_processing_seconds", "Time spent processing requests")
FAILED_REQUESTS = Counter("whirly_failed_requests_total", "Total failed requests")
LOGIN_ATTEMPTS = Counter("whirly_login_attempts_total", "Total login attempts")
ACTIVE_USERS = Gauge("whirly_active_users_total", "Current active users")

def setup_metrics(port=8002):
    start_http_server(port)
    print(f"Prometheus metrics server started at :{port}")

# Usage example in FastAPI or similar:
# @REQUEST_TIME.time()
# def endpoint(...):
#     ...
# FAILED_REQUESTS.inc() on exception
# LOGIN_ATTEMPTS.inc() on login attempt