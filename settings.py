import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LOGS_CHANNEL = os.getenv("LOGS_CHANNEL")
SPECIAL_ROLE = os.getenv("SPECIAL_ROLE")
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')