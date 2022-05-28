
# checks if the author of the new message is the author of the command, also in same channel
def check(author, ctx):
    def innerCheck(message):
        return message.author == author and message.channel == ctx.channel
    return innerCheck

