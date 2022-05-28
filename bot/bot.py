
# bot.py

import os
import urllib

from discord.ext import commands
from dotenv import load_dotenv

import utils.utilities as util
import utils.rankUtil as rws
import utils.jsonUtil as jsu

os.chdir('C:/Users/Lucas/Documents/Inhouses/bot')

commandPrefix = '!'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix=commandPrefix)

@bot.event
async def on_ready():

    print(f'{bot.user.name} has connected to discord')


@bot.command("setup")
async def set_rank(ctx, *args):

    if util.check(ctx.author, ctx):

        ign = ' '.join(args)

        rank = rws.get_Rank(ign)

        if(rank == ""):
            await ctx.send("There is no ign with a rank, please check your spelling you dumb fuck")
            return

        emojis = ['✅', '❌']

        message = await ctx.send("Your Rank is **" + rank + "**\nIs this correct?")

        for emoji in emojis:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.message.author and reaction.message == message
        
        reaction = await bot.wait_for("reaction_add", check=check)  # Wait for a reaction

        if str(reaction[0]) == '✅':
            
            jsu.setup(userid=str(ctx.author.id),ign=ign,rank=rank)

            await ctx.send("Added player **" + ign + "** with rank **" + rank + "**")

        if str(reaction[0]) == '❌':

            await ctx.send("Please restart with the proper ign\nOr make sure to update your u.gg found at https://u.gg/lol/profile/na1/" + urllib.parse.quote(ign) + "/overview")

# 5 v 5 lobby, automatically balanced based on rank, then decide winners and losers, winners increment wins, losers increment loss, win/win+loss for winrate












bot.run(TOKEN)