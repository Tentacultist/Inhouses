
# bot.py

import os
import urllib
from datetime import date, datetime

import discord
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
@bot.command("lobby")
async def createLobby(ctx):

    datestr = date.today().strftime("%m/%d/%Y")
    timestr = datetime.now().strftime("%H:%M")


    embed=discord.Embed(title="League 5v5" , url="https://github.com/Tentacultist/Inhouses", description="5v5 Lobby created at " + timestr + " on " +  datestr, color=0x006cfa)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://pentagram-production.imgix.net/cc7fa9e7-bf44-4438-a132-6df2b9664660/EMO_LOL_02.jpg?rect=0%2C0%2C1440%2C1512&w=640&crop=1&fm=jpg&q=70&auto=format&fit=crop&h=672")
    
    playerlist = [ctx.author.display_name,"---------","---------","---------","---------","---------","---------","---------","---------","---------"]
    playeridlist = [ctx.author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    embed.add_field(name="Queued Players", value="{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(playerlist[0], playerlist[1], playerlist[2], playerlist[3], playerlist[4], playerlist[5], playerlist[6], playerlist[7], playerlist[8], playerlist[9]), inline=True)

    await ctx.send(embed=embed)

    

# leaderboard 

# past lobbies :^)

bot.run(TOKEN)