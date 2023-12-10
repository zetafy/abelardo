import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")
GUILD_ID = os.getenv("GUILD_ID")