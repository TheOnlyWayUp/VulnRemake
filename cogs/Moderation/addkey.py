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
      db[key] = value
      await ctx.reply(f"Set {key} to {value}", delete_after=db["del"])
    await ctx.message.delete()