import discord, aiohttp, os
from replit import db
from discord.ext import commands

key_of_the_api = os.environ["api"]
class apicheck(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Checks if the API is functional.")
  async def api_check(ctx):
    async with aiohttp.ClientSession() as session:
      async with session.get(f'https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2') as resp:
        x = await resp.json()
    if x["success"] is True:
      await ctx.reply("Request successful.")
    elif x["success"] is False:
      await ctx.reply(f"Request failed, reason - {x['cause']}")

def setup(bot):
    bot.add_cog(apicheck(bot))