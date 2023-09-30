import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LOGS_CHANNEL = os.getenv("LOGS_CHANNEL")
SPECIAL_ROLE = os.getenv("SPECIAL_ROLE")