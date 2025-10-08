import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import re
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🎲 {bot.user} est en ligne!')
    await bot.tree.sync()
    print('✅ Commandes prêtes!')

@bot.tree.command(name="r", description="Lance des dés (ex: 1d20, 2d6+5)")
async def roll(interaction: discord.Interaction, des: str):
    # Parser: XdY+Z ou XdY-Z ou XdY
    match = re.match(r'(\d+)?d(\d+)([+\-]\d+)?', des.lower().replace(' ', ''))
    
    if not match:
        await interaction.response.send_message("❌ Format: `1d20` ou `2d6+5`", ephemeral=True)
        return
    
    # Extraire les valeurs
    nombre = int(match.group(1) or 1)
    faces = int(match.group(2))
    bonus = int(match.group(3) or 0)
    
    # Lancer les dés
    jets = [random.randint(1, faces) for _ in range(nombre)]
    total = sum(jets) + bonus
    
    # Affichage des résultats
    details = ' + '.join([f"`{j}`" for j in jets])
    if bonus != 0:
        details += f" {'+' if bonus > 0 else ''} `{bonus}`"
    
    # Message
    resultat = f"🎲 **{des}**\n{details}\n\n**Total: {total}**"
    
    await interaction.response.send_message(resultat)

bot.run(TOKEN)