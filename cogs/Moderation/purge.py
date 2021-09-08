import discord
from replit import db
from discord.ext import commands
from main import stcheck

class purge(commands.Cog, name="Purge"):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Purges a given number of messages, defaults to 15")
  async def purge(self, ctx, amount=30):
    if await stcheck(ctx) is True:
      channel = ctx.message.channel
      messages = []
      async for message in channel.history(limit=amount + 1):
        messages.append(message)
      await channel.delete_messages(messages)
      await ctx.send(embed=discord.Embed(title=f'{amount} messages have been purged by {ctx.message.author.name}', color=discord.Colour.random()), delete_after=db["del"])
    else:
      await ctx.reply("Not staff.")
def setup(bot):
    bot.add_cog(purge(bot))