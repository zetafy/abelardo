import discord
from discord import app_commands
from discord.ext import commands
from settings import GUILD_ID
import random
import math

# -------------------------------- ModuleNotFoundError Handler --------------------------------

class FixedPointQuestionsErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(COG Loaded): fixed_point_questions.py")
        
async def setup(bot):
    await bot.add_cog(FixedPointQuestionsErrorHandler(bot), guilds=[discord.Object(id=GUILD_ID)])
    
# -------------------------------- Questions --------------------------------

def fixed_to_dec_question():
    """
    Question of type 'convert a fixed-point number to its decimal representation'
    """
    n = random.randint(6, 12)
    fixed_point_number = "".join(str(random.randint(0, 1)) for _ in range(n))
    no_of_int_bits = math.ceil(n * (2/3))
    no_of_frac_bits = math.floor(n * (1/3))
    
    integer_slice = fixed_point_number[:no_of_int_bits]
    fractional_slice = fixed_point_number[no_of_int_bits:]
    
    integer = int(integer_slice, 2)
    
    fraction = 0
    i = 0
    while i < len(fractional_slice):
        bit = fractional_slice[i]
        if bit == "1":
            fraction += (2 ** (-1 * (i + 1)))
        i += 1
        
    correct_answer = integer + fraction
    question = f"Given a fixed-point system with {no_of_int_bits} integer bits and {no_of_frac_bits} fractional bits, what is the decimal representation of the fixed-point number {fixed_point_number}"

    return question, correct_answer

def dec_to_fixed_question():
    """
    Question of type 'convert a decimal number to its fixed-point representation'
    """
    int_powers = [2**0, 2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9]
    frac_powers = [2**-1, 2**-2, 2**-3, 2**-4, 2**-5]
    
    a = random.randint(3, len(int_powers))
    b = random.randint(0, len(frac_powers))
    
    int_sample = random.sample(int_powers, a)
    integer = sum(int_sample)
    if b != 0:
        frac_sample = random.sample(frac_powers, b)
        fraction = sum(frac_sample)
        fractional_slice = ""
        for power in frac_powers:
            fractional_slice += "1" if power in frac_sample else "0"
    else:
        fractional_slice = ""
        frac_sample = []
        fraction = 0
        
    decimal_num = integer + fraction

    integer_slice = bin(integer)
    
    if fractional_slice == "":
        correct_answer = integer_slice + fractional_slice
    else:
        correct_answer = integer_slice + "." + fractional_slice
    
    question = f"What is the fixed-point representation of the decimal number {decimal_num}? If your answer includes a fractional part, please separate the integer and fractional parts with a dot '.' (eg. 3.5 = 11.1)"
    
    return question, correct_answer