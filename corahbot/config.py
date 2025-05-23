"""
Configuration settings for the CorahBot
"""

import os
from pathlib import Path

# Device configuration
DEVICE = "Android://127.0.0.1:5037/192.168.240.112:5555"

# Threshold values for template matching
THRESH_DEFAULT = 0.4
THRESH_ATTACK = 0.7

# Paths
BASE_DIR = Path(os.path.expanduser("~/bots"))
IMG_DIR = BASE_DIR / "imgs"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [IMG_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Bot settings
RETRY_LIMIT = 3
STANDARD_PAUSE = 0.5
LONG_PAUSE = 2.0
DEBUG_MODE = True

# API settings (optional)
API_HOST = "127.0.0.1"
API_PORT = 8000
