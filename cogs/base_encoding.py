import discord
from discord import app_commands
from discord.ext import commands
from settings import GUILD_ID
from .base_encoding_questions import base_encoding_question

# -------------------------------- ModuleNotFoundError Handler --------------------------------

class BaseEncodingErrorHandler(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(COG Loaded): base_encoding.py")
        
async def setup(bot):
    await bot.add_cog(BaseEncodingErrorHandler(bot), guilds=[discord.Object(id=GUILD_ID)])
    
# -------------------------------- review/Base Encoding UI --------------------------------

class AnswerModal(discord.ui.Modal, title="Submission"):
    """
    Answer submission form
    """ 
    answer = discord.ui.TextInput(label="Your Answer")
    def __init__(self, base_encoding_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_encoding_instance = base_encoding_instance

    async def on_submit(self, interaction: discord.Interaction):
        user_input = self.answer.value
        correct_answer = self.base_encoding_instance.correct_answer
        if user_input.lower() in [correct_answer.lower(), correct_answer[2:].lower()]:
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

class BaseEncoding():

    def __init__(self, review_callback):
        self.review_callback = review_callback
        self.title = "Base Encoding"
        self.color = discord.Colour.dark_orange()
        self.description = "Click 'Generate Question' to get started!"
        self.embed = None
        self.view = None
        self.correct_answer = None
        self.fields = 0
        
    def generate_embed(self):
        """
        Generate an `Embed` object for the UI of `/review/Base Encoding`
        """
        embed = discord.Embed(title=self.title, description=self.description, color=self.color)
        
        return embed
        
    def generate_view(self):
        """
        Generate a `View` object (consisting of buttons) for the UI of `/review/Base Encoding`
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
        Generate a random base encoding question
        """
        question, correct_answer = base_encoding_question()
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