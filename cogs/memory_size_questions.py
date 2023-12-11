import discord
from discord import app_commands
from discord.ext import commands
from settings import GUILD_ID
import random
import math

# -------------------------------- ModuleNotFoundError Handler --------------------------------

class MemorySizeQuestionsErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(COG Loaded): memory_size_questions.py")
        
async def setup(bot):
    await bot.add_cog(MemorySizeQuestionsErrorHandler(bot), guilds=[discord.Object(id=GUILD_ID)])
    
# -------------------------------- Questions --------------------------------

UNITS = ["bytes", "kilobytes", "megabytes"]

def total_size_question():
    """
    Memory size question generator (type: total size)
    """
    n = random.randint(8, 32) # in bits
    m = random.randint(2, 32) # in bytes
    
    correct_answer = (2 ** n) * m
    
    answer_in_unit = random.choice(UNITS)
    if answer_in_unit == "kilobytes":
        correct_answer /= (2 ** 10)
    elif answer_in_unit == "megabytes":
        correct_answer /= (2 ** 20)
        
    if float(correct_answer).is_integer():
        correct_answer = int(correct_answer)
    
    question = f"What is the size of a memory with {n} address bits, and cells each sized {m} bytes? Your answer should be in {answer_in_unit}!"
    
    return question, correct_answer

def cell_size_question():
    """
    Memory size question generator (type: cell size)
    """
    total = 2 ** random.randint(16, 24)
    n = random.randint(12, 16)
    
    correct_answer = total / (2 ** n)
    
    total_in_unit = random.choice(UNITS)
    if total_in_unit == "kilobytes":
        total /= (2 ** 10)
    elif total_in_unit == "megabytes":
        total /= (2 ** 20)
    
    if float(total).is_integer():
        total = int(total)
        
    if float(correct_answer).is_integer():
        correct_answer = int(correct_answer)
        
    question = f"What is the size of each cell in a memory sized {total} {total_in_unit} with {n} address bits? Your answer should be in bytes!"
        
    return question, correct_answer

def no_of_cells_question():
    """
    Memory size question generator (type: number of cells)
    """
    m = random.randint(2, 32)
    power_of_2 = random.randint(16, 24) # This ensures 'total' is a multiple of 'm'
    total = 2 ** power_of_2 * m

    correct_answer = total / m  # This will always be an integer
    
    total_in_unit = random.choice(UNITS)
    if total_in_unit == "kilobytes":
        total /= (2 ** 10)
    elif total_in_unit == "megabytes":
        total /= (2 ** 20)
        
    if float(correct_answer).is_integer():
        correct_answer = int(correct_answer)    
        
    if float(total).is_integer():
        total = int(total)
        
    question = f"How many cells are there in a memory sized {total} {total_in_unit} where each cell is {m} bytes?"
    return question, correct_answer

def address_bits_question():
    """
    Memory size question generator (type: number of address bits)
    """
    m = 2 ** random.randint(1, 5)  # ensures to give a value of m that is a power of 2 between 2 and 32

    power_of_2 = random.randint(16, 24)
    total = 2 ** power_of_2 * m

    correct_answer = math.log((total / m), 2)
    
    total_in_unit = random.choice(UNITS)
    if total_in_unit == "kilobytes":
        total /= (2 ** 10)
    elif total_in_unit == "megabytes":
        total /= (2 ** 20)
        
    if float(correct_answer).is_integer():
        correct_answer = int(correct_answer)    
        
    if float(total).is_integer():
        total = int(total)
        
    question = f"How many bits are needed to encode the addresses of a memory sized {total} {total_in_unit} where each cell is {m} bytes?"
    return question, correct_answer