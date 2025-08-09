from loguru import logger

def setup_logging(log_file="app.log"):
    logger.remove()
    logger.add(log_file, rotation="1 week", retention="1 month", level="INFO")
    logger.add(lambda msg: print(msg, end=""), level="ERROR")

def error_wrapper(func):
    """Decorator to handle errors and log them."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            raise
    return wrapper