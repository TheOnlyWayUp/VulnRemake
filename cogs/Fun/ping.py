import discord
from replit import db
from discord.ext import commands

class ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  async def ping(self, ctx):
    await ctx.reply(embed=discord.Embed(title="Pong!", description=f"Your ping is {round(self.bot.latency * 1000)}ms.", color=0x39f220))