import discord
from discord import app_commands
from discord.ext import commands
from settings import GUILD_ID
from .data import TOPICS
from .base_encoding import BaseEncoding
from .memory_size import MemorySize

class Review(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("(COG Loaded): review.py")
        
    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"(SYNC): Successfuly synced {len(fmt)} commands.")
        
    @app_commands.command(name="question2", description="questions form")
    async def question2(self, interaction: discord.Interaction, question: str):
        await interaction.response.send_message("PONG")
        
    @app_commands.command(name="review", description="Review for ELEC1601")
    async def review(self, interaction: discord.Interaction):
        """
        Entry-point to using the Abelardo BOT; displays a list of
        ELEC1601 topics for the user to choose from.
        """
        # -------------------------------- Callbacks --------------------------------
        # `Go Back` callback
        async def review_callback(interaction):
            await interaction.response.edit_message(view=review_view, embed=review_embed)
            
        async def topics_dropdown_callback(interaction):
            chosen_topic = interaction.data['values'][0]

            # Base encoding callback
            if chosen_topic == TOPICS[0]:
                topic = BaseEncoding(review_callback=review_callback)
                embed = topic.generate_embed()
                view = topic.generate_view()
            
            # Fixed point callback
            elif chosen_topic == TOPICS[1]:
                pass
            
            # Memory size callback
            elif chosen_topic == TOPICS[2]:
                topic = MemorySize(review_callback=review_callback)
                embed = topic.generate_embed()
                view = topic.generate_view()
            
            else:
                print("[!] Topic Not Found!")
                await interaction.response.send_message("[!] Topic Not Found!")
                
            await interaction.response.edit_message(embed = embed, view = view)
            
        # -------------------------------- User interface for `/review` --------------------------------
            
        review_embed = discord.Embed(title="ELEC1601 Question Generator", description="What topic would you like to review?", color=discord.Colour.dark_orange())
        review_embed.set_image(url="https://i.ibb.co/sQQG748/UNIVERSITY.png")
        
        review_view = discord.ui.View()
        
        options = []
        for topic in TOPICS:
            option = discord.SelectOption(label=topic, value=topic)
            options.append(option)
            
        topics_dropdown = discord.ui.Select(placeholder="Select a topic", options=options)
        topics_dropdown.callback = topics_dropdown_callback
        review_view.add_item(topics_dropdown)
            
        await interaction.response.send_message(embed=review_embed, view=review_view)
        
async def setup(bot):
    await bot.add_cog(Review(bot), guilds=[discord.Object(id=GUILD_ID)])