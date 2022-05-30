
# bot.py

import os
import urllib
from datetime import date, datetime
import time

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
            await ctx.send("There is no ign with a rank, either you didn't input an ign, or check your spelling")
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

            return

        if str(reaction[0]) == '❌':

            await ctx.send("Please restart with the proper ign\nOr perhaps you might have decayed recently")

            return

# 5 v 5 lobby, automatically balanced based on rank, then decide winners and losers, winners increment wins, losers increment loss, win/win+loss for winrate
@bot.command("lobby")
async def createLobby(ctx):

    datestr = date.today().strftime("%m/%d/%Y")
    timestr = datetime.now().strftime("%H:%M")
    description = "5v5 Lobby created at " + timestr + " on " +  datestr + "\n\n**For Players**\nTo join, react with ✅\nTo leave, react with ❌\n\n**For Lobby Leader**\nTo close the lobby, react with 😭\n To begin match, react with 💢\n"
    
    embed=discord.Embed(title="League 5v5 Lobby" , url="https://github.com/Tentacultist/Inhouses", description=description, color=0x006cfa)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://pentagram-production.imgix.net/cc7fa9e7-bf44-4438-a132-6df2b9664660/EMO_LOL_02.jpg?rect=0%2C0%2C1440%2C1512&w=640&crop=1&fm=jpg&q=70&auto=format&fit=crop&h=672")
    
    playerlist = [ctx.message.author.name,"---------","---------","---------","---------","---------","---------","---------","---------","---------"]
    playeridlist = [ctx.author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    embed.add_field(name="Queued Players", value="{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(*playerlist), inline=True)

    msg = await ctx.send(embed=embed)

    #after embed created, need loop to add players and id to the list, up to 10 players
    emojis = ['✅', '❌', '😭', '💢']

    for emoji in emojis:
        await msg.add_reaction(emoji)

    def checkReaction(reaction, user):
        return reaction.message == msg and user != msg.author

 
    while(True):

        reaction = await bot.wait_for("reaction_add", check=checkReaction)

        userid = reaction[1].id
        user = await bot.fetch_user(userid)
        usernick = user.display_name

        # closes lobby
        if str(reaction[0]) == '😭' and userid == ctx.author.id:
            
            descriptionClosed = "Restart lobby with `!lobby`\nOr you guys can touch grass\n"
            embedClosed = discord.Embed(title="Lobby Closed", description=descriptionClosed)
            await msg.edit(embed=embedClosed)

            for emoji in emojis:
                await msg.clear_reaction(emoji)

            return
        
        if str(reaction[0]) == '✅':
            
            # user is already in lobby
            if userid in playeridlist:
                
                await ctx.send("You are already queued up")
                await msg.remove_reaction(reaction[0], user)
                continue
            
            # lobby has 10 players
            if playeridlist[9] != 0:

                await ctx.send("Lobby is Full")
                await msg.remove_reaction(reaction[0], user)
                continue
            
            firstOpen = 0

            for playerid in playeridlist:
                if playerid == 0:
                    break
                else:
                    firstOpen += 1

            playerlist[firstOpen] = usernick
            playeridlist[firstOpen] = userid

            # embed stuff
            embedAdd=util.embedEdit(ctx, playerlist)
            
            await msg.edit(embed=embedAdd)

            await msg.remove_reaction(reaction[0], user)
        
        if str(reaction[0]) == '❌':
            
            if(userid not in playeridlist):
                await ctx.send("You are not in the queue")
                await msg.remove_reaction(reaction[0], user)
                continue

            playeridlist.remove(userid)
            playeridlist.append(0)

            playerlist.remove(usernick)
            playerlist.append("---------")

            embedAdd = util.embedEdit(ctx, playerlist)
            
            await msg.edit(embed=embedAdd)

            await msg.remove_reaction(reaction[0], user)

        # splits list of players into 2 and then displays
        if str(reaction[0]) == '💢' and userid == ctx.author.id:
            
            if playeridlist[9] == 0:

                await ctx.send("There are not enough players in the queue")
                await msg.remove_reaction(reaction[0], user)
                continue

            playerRVList = []

            for id in playeridlist:
                if(id != 0):
                    playerRVList.append(rws.rankValue(jsu.getRank(id)))

            # returns 2 teams of relatively equal strength, the player ids
            teamOne,teamTwo = util.splitTeams(playeridlist, playerRVList)

            print(teamOne)
            print(teamTwo)

            for emoji in emojis:
                await msg.clear_reaction(emoji)
            
            gameEmojis = ["✋", "🟦", "🟥"]

            for emoji in gameEmojis:
                await msg.add_reaction(emoji)

            gameDescription = "**Match Start!** Good luck and have fun\n\n**For Lobby Leader**\nTo cancel match, react with ✋\n Blue team win, 🟦\nRed team win, 🟥"

            embedGame=discord.Embed(title="League 5v5 Match" , url="https://github.com/Tentacultist/Inhouses", description=gameDescription, color=0x006cfa)
            embedGame.set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
            embedGame.set_thumbnail(url="https://pentagram-production.imgix.net/cc7fa9e7-bf44-4438-a132-6df2b9664660/EMO_LOL_02.jpg?rect=0%2C0%2C1440%2C1512&w=640&crop=1&fm=jpg&q=70&auto=format&fit=crop&h=672")
            
            embedGame.add_field(name="Team One", value="{}\n{}\n{}\n{}\n{}".format(*teamOne), inline=True)
            embedGame.add_field(name="Team Two", value="{}\n{}\n{}\n{}\n{}".format(*teamTwo), inline=True)

            await msg.edit(embed=embedGame)

            while(True):

                reaction = await bot.wait_for("reaction_add", check=checkReaction)

                if str(reaction[0]) == '✋' and userid == ctx.author.id:
            
                    descriptionMatchClosed = "Match has been canceled, Touch Grass"
                    embedClosed = discord.Embed(title="Match Closed", description=descriptionMatchClosed)
                    await msg.edit(embed=embedClosed)

                    for emoji in gameEmojis:
                        await msg.clear_reaction(emoji)

                    return
                
                if (str(reaction[0]) == '🟦' or str(reaction[0]) == '🟥') and userid == ctx.author.id:
                    
                    if str(reaction[0]) == '🟦':

                        jsu.incrementWin(teamOne)
                        jsu.incrementLoss(teamTwo)


                    if str(reaction[0]) == '🟥':

                        jsu.incrementWin(teamTwo)
                        jsu.incrementLoss(teamOne)

                    descriptionMatchClosed = "Match is over **GG**"
                    embedClosed = discord.Embed(title="Match Closed", description=descriptionMatchClosed)
                    await msg.edit(embed=embedClosed)

                    for emoji in gameEmojis:
                        await msg.clear_reaction(emoji)

                    return



# at any number of people, will split the players in half based on rank lp, need to make module to determine rank/number associated, use algo to return

# leaderboard 
@bot.command("leaderboard")
async def leaderboard(ctx):
    print("leaderboard")


@bot.command("profile")
async def profile(ctx):
    
    userid = ctx.author.id

    gameDescription = "NGL not that impressive"

    userIgn, userRank, userWin, userLoss, userWR, userlp = jsu.getPlayerData(userid)

    embedUser=discord.Embed(title=ctx.author.display_name , url="https://github.com/Tentacultist/Inhouses", description=gameDescription, color=0x006cfa)
    embedUser.set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
    embedUser.set_thumbnail(url=ctx.author.avatar_url)

    embedUser.add_field(name="IGN", value=userIgn, inline=False)
    embedUser.add_field(name="Rank", value=userRank, inline=True)
    embedUser.add_field(name="Wins", value=userWin, inline=True)
    embedUser.add_field(name="Losses", value=userLoss, inline=True)
    embedUser.add_field(name="Winrate", value=userWR, inline=True)
    embedUser.add_field(name="LP", value=userlp, inline=True)

    msg = await ctx.send(embed=embedUser)


# past lobbies :^)

bot.run(TOKEN)