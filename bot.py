import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp  
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Connecté en tant que {bot.user}')

@bot.command()
async def bonjour(ctx):
    embed = discord.Embed(
        title="👋 Bonjour !",
        description=f"Salut {ctx.author.mention}, j’espère que tu vas bien !",
        color=discord.Color.yellow()
    )
    embed.set_footer(text="🍮 ૮ ・ﻌ・ა")
    await ctx.send(embed=embed)

@bot.command() 
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
            if resp.status != 200:
                await ctx.send("😿 Impossible de récupérer une image de chat.")
                return
            data = await resp.json()
            image_url = data[0]["url"]

            embed = discord.Embed(
                title="🐾 Voici un chat trop mignon :",
                color=discord.Color.yellow()
            )
            embed.set_image(url=image_url)
            embed.set_footer(text="Fourni par TheCatAPI 🐱")

            await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)  
async def clear(ctx, amount: int):
    """Supprime un certain nombre de messages dans le salon"""
    
    if amount < 1:
        await ctx.send("⚠️ Tu dois supprimer au moins **1** message.")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1) 

    embed = discord.Embed(
        title="🧹 Messages supprimés",
        description=f"**{len(deleted) - 1}** messages ont été supprimés dans {ctx.channel.mention}.",
        color=discord.Color.yellow()
    )
    embed.set_footer(text=f"Action effectuée par {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed, delete_after=5) 

@bot.command()
async def pokemon(ctx):
    """Affiche un Pokémon aléatoire avec possibilité de shiny"""
    max_pokemon = 1010
    poke_id = random.randint(1, max_pokemon)
    
    shiny_chance = 0.05  # 5% de chance d'être shiny (modifiable)
    is_shiny = random.random() < shiny_chance  # True si shiny
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}") as resp:
            if resp.status != 200:
                await ctx.send("⚠️ Impossible de récupérer un Pokémon.")
                return
            data = await resp.json()
            
            name = data['name'].capitalize()
            types = [t['type']['name'].capitalize() for t in data['types']]
            
            # Choisir l'image normale ou shiny
            sprite_url = data['sprites']['front_shiny'] if is_shiny else data['sprites']['front_default']

            embed = discord.Embed(
                title=f" Pokémon aléatoire : {name}{' ✨Shiny✨' if is_shiny else ''}",
                description=f"**Type(s) :** {', '.join(types)}",
                color=discord.Color.yellow()
            )
            if sprite_url:
                embed.set_image(url=sprite_url)
            embed.set_footer(text=f"Données fournies par PokéAPI | {'Shiny' if is_shiny else 'Normal'}")

            await ctx.send(embed=embed)


bot.run(TOKEN)
