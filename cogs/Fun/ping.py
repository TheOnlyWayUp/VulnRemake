import discord
from replit import db
from discord.ext import commands

class Ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Pings the bot and returns latency.")
  async def ping(self, ctx):
    await ctx.reply(embed=discord.Embed(title="Pong!", description=f"Your ping is {round(self.bot.latency * 1000)}ms.", color=0x39f220), delete_after=db["del"])
    await ctx.message.delete()
def setup(bot):
  bot.add_cog(Ping(bot))