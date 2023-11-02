import os
from dotenv import load_dotenv

load_dotenv()
# PREFIX_BOT = ['h','H'] #test
PREFIX_BOT = ['v','V'] #main 
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')