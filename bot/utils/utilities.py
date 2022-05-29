import discord
from discord.ext import commands
from datetime import date, datetime



# checks if the author of the new message is the author of the command, also in same channel
def check(author, ctx):
    def innerCheck(message):
        return message.author == author and message.channel == ctx.channel
    return innerCheck

def embedEdit(ctx, playerlist: list) -> discord.Embed:

    datestr = date.today().strftime("%m/%d/%Y")
    timestr = datetime.now().strftime("%H:%M")
    description = "5v5 Lobby created at " + timestr + " on " +  datestr + "\n\n**For Players**\nTo join, react with ✅\nTo leave, react with ❌\n\n**For Lobby Leader**\nTo close the lobby, react with 😭\n To begin match, react with 💢\n"

    embedAdd=discord.Embed(title="League 5v5" , url="https://github.com/Tentacultist/Inhouses", description=description, color=0x006cfa)
    embedAdd.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embedAdd.set_thumbnail(url="https://pentagram-production.imgix.net/cc7fa9e7-bf44-4438-a132-6df2b9664660/EMO_LOL_02.jpg?rect=0%2C0%2C1440%2C1512&w=640&crop=1&fm=jpg&q=70&auto=format&fit=crop&h=672")
    embedAdd.add_field(name="Queued Players", value="{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(*playerlist), inline=True)
    
    return embedAdd

