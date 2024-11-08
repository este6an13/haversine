import structlog
import logging

# Configure standard logging to integrate with structlog
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)

# Define processors that modify log records before they are emitted
processors = [
    structlog.processors.KeyValueRenderer(
        key_order=["timestamp", "event", "app_name", "user_id"]
    ),
    structlog.processors.TimeStamper(fmt="iso"),  # Add timestamp in ISO format
]

# Add context to all logs with the app_name
log = structlog.get_logger()
log = log.bind(app_name="my_app")


def get_logger():
    """
    Returns the logger with pre-configured processors and context.
    """
    return log
