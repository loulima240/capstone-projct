
"""
Central configuration.

Everything you change often lives here, not scattered across the code.
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from the project root
load_dotenv(Path(__file__).resolve().parent / ".env")

# Support UTF-8 characters and emojis
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# Anthropic API configuration
API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model configuration
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")

# Response configuration
TEMPERATURE = 0.7
MAX_TOKENS = 1024

# Logging configuration
logging.getLogger("anthropic").setLevel(logging.WARNING)

