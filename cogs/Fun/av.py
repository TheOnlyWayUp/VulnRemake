import discord
from replit import db
from discord.ext import commands

class getAv(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Gets the avatar of a user", aliases=["av"])
  async def avatar(ctx, member: discord.Member=None):
    if member is None:
      nonebed = discord.Embed(title="You need to mention a member!",color=0xea5852)
      await ctx.reply(embed=nonebed, delete_after=db["del"])
def setup(bot):
  bot.add_cog(getAv(bot))