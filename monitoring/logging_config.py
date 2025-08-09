import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="app.log"):
    logger = logging.getLogger("whirly")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Sentry integration (optional)
# import sentry_sdk
# sentry_sdk.init(dsn="your_sentry_dsn_here")