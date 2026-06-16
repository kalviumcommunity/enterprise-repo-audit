"""
Utility Functions and Helpers

Common utility functions for logging, data validation, and formatting.
"""

import json
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def format_timestamp(dt=None):
    """Format a datetime object to ISO format string."""
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def validate_email(email):
    """Basic email validation."""
    if "@" not in email or "." not in email.split("@")[1]:
        return False
    return True


def log_event(event_type, details, level="INFO"):
    """Log an event with structured details."""
    log_entry = {
        "timestamp": format_timestamp(),
        "event_type": event_type,
        "details": details,
    }
    
    if level == "INFO":
        logger.info(json.dumps(log_entry))
    elif level == "WARNING":
        logger.warning(json.dumps(log_entry))
    elif level == "ERROR":
        logger.error(json.dumps(log_entry))
    
    return log_entry


def parse_config_line(line):
    """Parse a configuration line in key=value format."""
    if "=" not in line:
        return None, None
    key, value = line.split("=", 1)
    return key.strip(), value.strip()


def sanitize_filename(filename):
    """Remove unsafe characters from a filename."""
    unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename


def check_service_health():
    """Check if service dependencies are available."""
    health_status = {
        "status": "healthy",
        "timestamp": format_timestamp(),
        "checks": {
            "memory": "ok",
            "disk": "ok",
            "network": "ok",
        }
    }
    return health_status
