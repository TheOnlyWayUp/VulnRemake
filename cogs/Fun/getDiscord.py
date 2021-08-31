import discord
from replit import db
from discord.ext import commands
from main import *

class getDiscord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(help="Finds the Discord of a user, if paired through their Minecraft username.")
    async def getDiscord(ctx, user=None):
      if user is None:
        await ctx.send("Correct usage - `v!discord <MC_Username>`.")
      else:
        if await returnExistence(user) is True:
          try:
            disc = await returnDiscord(user)
            await ctx.send(embed=discord.Embed(title=f"{user}'s Discord is {disc}.", description=f"Run by {ctx.author.name}.",color=0x96cdcd), delete_after=db["del"])
          except:
            await ctx.send(embed=discord.Embed(title=f"{user}'s Discord is not linked.", description=f"Run by {ctx.author.name}.", color=0xf08080), delete_after=db["del"])
        else:
          await ctx.send("User does not exist!")