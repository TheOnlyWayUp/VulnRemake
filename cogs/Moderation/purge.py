import discord
from replit import db
from discord.ext import commands
from main import stcheck

class purge(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Purges a given number of messages, defaults to 15")
  async def purge(ctx, amount=30):
    if await stcheck(ctx) is True:
      channel = ctx.message.channel
      messages = []
      async for message in channel.history(limit=amount + 1):
        messages.append(message)
      await channel.delete_messages(messages)
      await ctx.send(f'{amount} messages have been purged by {ctx.message.author.mention}')
    else:
      await ctx.reply("Not staff.")
def setup(bot):
    bot.add_cog(purge(bot))