"""Logging configuration using loguru"""

import os
import sys
from pathlib import Path
from loguru import logger

# Remove default handler
logger.remove()

# Get logging configuration from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Console output format
console_format = (
    "<level>{level: <8}</level> | "
    "<cyan>{name:<25}</cyan> | "
    "<level>{message}</level>"
)

# File output format
file_format = (
    "<level>{level: <8}</level> | "
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "<cyan>{name}:{function}:{line}</cyan> | "
    "<level>{message}</level>"
)

# Console handler (stdout)
logger.add(
    sys.stdout,
    format=console_format,
    level=LOG_LEVEL,
    colorize=True,
)

# File handler - general logs
logger.add(
    logs_dir / "app.log",
    format=file_format,
    level=LOG_LEVEL,
    rotation="100 MB",  # Rotate when file reaches 100MB
    retention="7 days",  # Keep logs for 7 days
    compression="zip"  # Compress old logs to ZIP
)

# File handler - scraper logs
logger.add(
    logs_dir / "scraper.log",
    format=file_format,
    level=LOG_LEVEL,
    filter=lambda record: "scraper" in record.get("name", "").lower(),
    rotation="100 MB",
    retention="7 days",
    compression="zip"
)

# File handler - database logs
logger.add(
    logs_dir / "database.log",
    format=file_format,
    level=LOG_LEVEL,
    filter=lambda record: "database" in record.get("name", "").lower(),
    rotation="100 MB",
    retention="7 days",
    compression="zip"
)

# File handler - error logs
logger.add(
    logs_dir / "errors.log",
    format=file_format,
    level="ERROR",
    rotation="100 MB",
    retention="30 days",
    compression="zip"
)

# Debug mode - add more verbose logging
if DEBUG:
    logger.add(
        logs_dir / "debug.log",
        format=file_format,
        level="DEBUG",
        backtrace=True,  # Include full stack traces
        diagnose=True  # Include local variables in errors
    )

# Suppress verbose third-party loggers
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {},
    "loggers": {
        "playwright": {"level": "WARNING"},
        "urllib3": {"level": "WARNING"},
        "selenium": {"level": "WARNING"},
        "crewai": {"level": "INFO"},
    }
}


def get_logger(name: str):
    """Get a logger instance"""
    return logger.bind(name=name)


# Export main logger
__all__ = ["logger", "get_logger"]
