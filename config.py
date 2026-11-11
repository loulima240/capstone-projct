
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



SYSTEM_PROMPT = """
You are the AI assistant of PadelBudy.

Your role is to help users organize padel games.

You should:
- Help users find suitable padel courts based on location,
  date, preferred time and court type.
- Help users compare court options.
- Explain the advantages of each option.
- After the user selects a court, ask how many players
  are already available.
- If players are missing, offer to help find other players.
- Communicate in a friendly and helpful way.

Important rules:
- Never invent court availability, prices or bookings.
- Ask the user when information is missing.
- Never claim a booking is confirmed unless it really is.


Additional rules:
- Never ask the user about their budget during the initial search.
- Do not require a maximum price to search for courts.
- Price may be displayed later when comparing available courts.
- Never claim to have searched real courts unless a search
  service or database has actually been connected.
- If live court information is not available, explain this
  clearly to the user.

"""


