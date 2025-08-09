import logging
from datetime import datetime

def log_audit_event(user_id, action, details, severity="INFO"):
    logger = logging.getLogger("whirly.audit")
    timestamp = datetime.utcnow().isoformat()
    logger.log(getattr(logging, severity), f"[{timestamp}] user={user_id} action={action} details={details}")

def get_audit_events(log_file="audit.log"):
    with open(log_file) as f:
        events = f.readlines()
    return events