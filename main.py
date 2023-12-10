import discord
from discord.ext import commands
import settings
import asyncio
import requests
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, application=settings.APPLICATION_ID)

@bot.event
async def on_ready():
    print("[*] Abelardo is now online!")
    
async def load():
    """
    Load COGs
    """
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    await load()
    await bot.start(settings.TOKEN)
    
asyncio.run(main())