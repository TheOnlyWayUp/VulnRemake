import discord
from replit import db
from discord.ext import commands

class getAv(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Gets the avatar of a user", aliases=["av"])
  async def avatar(self, ctx, member: discord.Member=None):
    if member is None:
      await ctx.reply(embed=discord.Embed(title="You need to mention a member!",color=0xea5852), delete_after=db["del"])
    else:
      avEm = discord.Embed(title="Lookin good!")
      avEm.set_image(url=member.avatar_url)
      await ctx.reply(embed=avEm, delete_after=db["del"])
    await ctx.message.delete()
def setup(bot):
  bot.add_cog(getAv(bot))