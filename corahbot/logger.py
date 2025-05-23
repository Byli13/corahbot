"""
Logging configuration for CorahBot
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from corahbot.config import LOG_DIR, DEBUG_MODE

def get_logger(name: str = "CorahBot"):
    """
    Configure and return a logger instance with both console and file handlers
    """
    logger = logging.getLogger(name)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = os.path.join(LOG_DIR, f"corahbot_{datetime.now():%Y%m%d}.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    return logger

# Create a default logger instance
log = get_logger()
