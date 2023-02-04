import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True

bot = discord.Bot(intents=intents, help_command=commands.DefaultHelpCommand())

@bot.command(description="For command testing")
@commands.has_role("Crp")
async def moretest(ctx,arg):
    """
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    """
    await ctx.respond("Hi! You just typed "+str(arg))