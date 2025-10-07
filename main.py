import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")

bot.run(TOKEN)