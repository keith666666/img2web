import logging
from logging.handlers import RotatingFileHandler

# Server Socket
bind = "0.0.0.0:5000"

# Worker Processes
workers = 3

# Timeout Settings
timeout = 120
graceful_timeout = 30

# Log Level
loglevel = "info"

# Paths to log files
access_log_path = "logs/access.log"  # Change to your desired log file path
error_log_path = "logs/error.log"  # Change to your desired log file path


# Custom Logging Configuration Hook
def on_starting(server):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Access Log Rotating File Handler
    access_log_handler = RotatingFileHandler(
        access_log_path, maxBytes=10485760, backupCount=5
    )
    access_log_handler.setFormatter(formatter)
    server.log.access_log.addHandler(access_log_handler)

    # Error Log Rotating File Handler
    error_log_handler = RotatingFileHandler(
        error_log_path, maxBytes=10485760, backupCount=5
    )
    error_log_handler.setFormatter(formatter)
    server.log.error_log.addHandler(error_log_handler)

    # Remove default handlers to avoid duplicate logging
    server.log.access_log.propagate = False
    server.log.error_log.propagate = False
