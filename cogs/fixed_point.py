import discord
from discord import app_commands
from discord.ext import commands
from settings import GUILD_ID
from .fixed_point_questions import fixed_to_dec_question, dec_to_fixed_question
import random

# -------------------------------- ModuleNotFoundError Handler --------------------------------

class FixedPointErrorHandler(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(COG Loaded): fixed_point.py")
        
async def setup(bot):
    await bot.add_cog(FixedPointErrorHandler(bot), guilds=[discord.Object(id=GUILD_ID)])
    
# -------------------------------- review/Memory Size UI --------------------------------

class AnswerModal(discord.ui.Modal, title="Submission"):
    """
    Answer submission form
    """ 
    answer = discord.ui.TextInput(label="Your Answer")
    def __init__(self, question_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question_instance = question_instance

    async def on_submit(self, interaction: discord.Interaction):
        user_input = self.answer.value
        correct_answer = self.question_instance.correct_answer
        type_of_question = self.question_instance.type_of_question
        if type_of_question == 1:
            if str(user_input) == str(correct_answer):
                title = "You Got It!"
                msg = f"You answered: {user_input}\n\nThat is correct!"
                msg += "\n\nClick 'Reveal Correct Answer' to verify!"
                color = discord.Colour.green()
            else:
                title = "Not Quite!"
                msg = f"You answered: {user_input}\n\nUnfortunately, that is incorrect!"
                msg += "\n\nClick 'Reveal Correct Answer' to view the correct answer!"
                color = discord.Colour.red()
        else:
            if str(user_input) in [correct_answer, correct_answer[2:]]:
                title = "You Got It!"
                msg = f"You answered: {user_input}\n\nThat is correct!"
                msg += "\n\nClick 'Reveal Correct Answer' to verify!"
                color = discord.Colour.green()
            else:
                title = "Not Quite!"
                msg = f"You answered: {user_input}\n\nUnfortunately, that is incorrect!"
                msg += "\n\nClick 'Reveal Correct Answer' to view the correct answer!"
                color = discord.Colour.red()
            
        embed = discord.Embed(title=title, description=msg, color=color)
        await interaction.response.send_message(embed = embed, ephemeral=True)

class FixedPoint():

    def __init__(self, review_callback):
        self.review_callback = review_callback
        self.title = "Fixed-Point Numbers"
        self.color = discord.Colour.dark_orange()
        self.description = "Click 'Generate Question' to get started!"
        self.embed = None
        self.view = None
        self.correct_answer = None
        self.fields = 0
        self.type_of_question = None
        
    def generate_embed(self):
        """
        Generate an `Embed` object for the UI of `/review/Fixed-Point Numbers`
        """
        embed = discord.Embed(title=self.title, description=self.description, color=self.color)
        
        return embed
        
    def generate_view(self):
        """
        Generate a `View` object (consisting of buttons) for the UI of `/review/Fixed-Point Numbers`
        """
        view = discord.ui.View()

        generate_btn = discord.ui.Button(style=discord.ButtonStyle.red, label="Generate Question")
        go_back_btn = discord.ui.Button(style=discord.ButtonStyle.gray, label="Go Back")
    
        buttons = [(generate_btn, self.generate_question),
                   (go_back_btn, self.review_callback)]
        
        for tup in buttons:
            button, callback_func = tup[0], tup[1]
            button.callback = callback_func
            view.add_item(item=button)
            
        return view
    
    async def generate_question(self, interaction):
        """
        Generate a random fixed-point numbers question
        """
        type_of_question = random.randint(1, 2)
        self.type_of_question = type_of_question
        
        if type_of_question == 1:
            question, correct_answer = fixed_to_dec_question()
        elif type_of_question == 2:
            question, correct_answer = dec_to_fixed_question()
        else:
            print("ERROR: Invalid question type!")
            
        msg = question + f"\n\nClick 'Submit Answer' when you're ready to answer!"
        embed = discord.Embed(title="Question", description=msg, color=self.color)

        view = discord.ui.View()
        submit_answer_btn = discord.ui.Button(style=discord.ButtonStyle.green, label="Submit Answer")
        reveal_answer_btn = discord.ui.Button(style=discord.ButtonStyle.red, label="Reveal Correct Answer")
        review_btn = discord.ui.Button(style=discord.ButtonStyle.gray, label="Go Back")

        buttons = [(submit_answer_btn, self.submit_answer),
                   (reveal_answer_btn, self.reveal_correct_answer),
                   (review_btn, self.review_callback)]

        for tup in buttons:
            button, callback_func = tup[0], tup[1]
            button.callback = callback_func
            view.add_item(item=button)
            
        self.embed, self.view, = embed, view
        self.correct_answer = correct_answer
        self.fields = 0

        await interaction.response.edit_message(embed = embed, view = view)
        
    async def submit_answer(self, interaction):
        """
        Send a pop-up modal for user to submit their answer.
        """
        modal = AnswerModal(self)
        await interaction.response.send_modal(modal)
    
    async def reveal_correct_answer(self, interaction):
        """
        Add a correct answer field to `generate_question` embed.
        """
        embed = self.embed
        if self.fields == 0:
            embed.add_field(name = "Correct Answer:", value = self.correct_answer)
            self.fields += 1
            
        view = self.view
        
        await interaction.response.edit_message(embed = embed, view = view)