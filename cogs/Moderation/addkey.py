import discord
from replit import db
from discord.ext import commands
from main import stcheck
class addkey(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Adds a key to the database.")
  async def addkey(self, ctx, key, *value:str):
    if await stcheck(ctx) is True:
      if key != "del":
        db[key] = value
        await ctx.reply(f"Set {key} to {value}", delete_after=db["del"])
      else:
        await ctx.reply("NAH, do v!delafter for that crap", delete_after=db["del"])
    await ctx.message.delete()
  @commands.command(help="Modifies the delete timer.")
  async def delafter(self, ctx, delf:int=5):
    if await stcheck(ctx) is True:
      db["del"] = delf
      await ctx.reply(f"Set the del_after to {delf}.", delete_after=db["del"])
    await ctx.message.delete()
def setup(bot):
  bot.add_cog(addkey(bot))