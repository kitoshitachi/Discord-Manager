import os
from dotenv import load_dotenv
import yaml

load_dotenv()
# PREFIX_BOT = ['h','H'] #test
PREFIX_BOT = 'v' #main 
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


try:
    with open('config.yml','r', encoding='utf-8') as f:
        CONFIG = yaml.load(f, Loader=yaml.FullLoader)
except UnicodeDecodeError:
    try:
        with open('config.yml','r', encoding='utf-8-sig') as f:
            CONFIG = yaml.load(f, Loader=yaml.FullLoader)
    except UnicodeDecodeError:
        with open('config.yml','r', encoding='latin-1') as f:
            CONFIG = yaml.load(f, Loader=yaml.FullLoader)