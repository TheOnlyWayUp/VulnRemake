import discord
from replit import db
from discord.ext import commands
from main import bot
from async_eval import eval
class Exec(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Executes the given arguement as python.", hidden=True)
  async def exec(self, ctx, *, to_exec):
    if ctx.author.id == 876055467678375998:
      try:
        eval(to_exec)
        await ctx.reply("Done.")
      except Exception as e:
        await ctx.reply(f"There was an error - {e}", delete_after=db["del"]*1.5)
def setup(bot):
  bot.add_cog(Exec(bot))