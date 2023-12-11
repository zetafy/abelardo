import discord
from discord import app_commands
from discord.ext import commands
from settings import GUILD_ID

# -------------------------------- ModuleNotFoundError Handler --------------------------------

class DataErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(COG Loaded): data.py")
        
async def setup(bot):
    await bot.add_cog(DataErrorHandler(bot), guilds=[discord.Object(id=GUILD_ID)])
    
# -------------------------------- DATA --------------------------------

TOPICS = [
    "Base encoding", # Generator
    "Fixed-point numbers", # Generator
    "Memory size", # Generator
]