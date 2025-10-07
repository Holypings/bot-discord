import os
from dotenv import load_dotenv
import discord
from discord.ext import commands


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté!')

bot.run(TOKEN)