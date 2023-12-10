import discord
from discord import app_commands
from discord.ext import commands
from settings import GUILD_ID
import random

# -------------------------------- ModuleNotFoundError Handler --------------------------------

class BaseEncodingQuestionsErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(COG Loaded): base_encoding_questions.py")
        
async def setup(bot):
    await bot.add_cog(BaseEncodingQuestionsErrorHandler(bot), guilds=[discord.Object(id=GUILD_ID)])
    
# -------------------------------- Questions --------------------------------

def base_encoding_question():
    bases = [2, 8, 10, 16]
    from_base, to_base = 0, 0

    # Ensure from_base and to_base are different
    while from_base == to_base:
        from_base = random.choice(bases)
        to_base = random.choice(bases)

    # Generate a random number
    number_to_convert = random.randint(100, 100000)
    print(f"Original number: {number_to_convert}")

    # Convert the number to the from_base
    if from_base == 2:
        number_to_convert = bin(number_to_convert)[2:]  # Remove '0b' prefix
        from_prefix = "0b"
    elif from_base == 8:
        number_to_convert = oct(number_to_convert)[2:]  # Remove '0o' prefix
        from_prefix = "0c"
    elif from_base == 10:
        from_prefix = ""
    elif from_base == 16:
        number_to_convert = hex(number_to_convert)[2:].upper()  # Remove '0x' prefix
        from_prefix = "0x"

    number_to_convert = str(number_to_convert)
    print(f"Number in base {from_base}: {number_to_convert}")

    # Convert the number to the to_base
    if to_base == 2:
        correct_answer = bin(int(number_to_convert, from_base))[2:]  # Convert and remove '0b'
        to_prefix = "0b"
    elif to_base == 8:
        correct_answer = oct(int(number_to_convert, from_base))[2:]  # Convert and remove '0o'
        to_prefix = "0c"
    elif to_base == 10:
        correct_answer = int(number_to_convert, from_base)           # Direct conversion
        to_prefix = ""
    elif to_base == 16:
        correct_answer = hex(int(number_to_convert, from_base))[2:].upper()  # Convert and remove '0x'
        to_prefix = "0x"

    question = f"What is the base {to_base} representation of the base {from_base} number {from_prefix}{number_to_convert}?"
    correct_answer = f"{to_prefix}{correct_answer}"
    
    return question, correct_answer