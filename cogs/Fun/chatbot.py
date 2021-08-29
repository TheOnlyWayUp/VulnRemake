import discord, prsaw2
from replit import db
from discord.ext import commands
pTalk = prsaw2.Client(key='Yfbjgiz58BIR')

class chatbot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Talk to an AI chatbot!", aliases=["s"])
  async def say(self, ctx, *msg):
    global inSesh
    try:
      await ctx.send(pTalk.get_ai_response(msg), delete_after=db["del"])
      inSesh=ctx.author.display_name
    except Exception as e:
      inSesh=None
      print(f"{ctx.author} tried '{msg}' but got {e}.")
      await ctx.send("There was an error, this has been reported to the dev.", delete_after=db["del"])
  @commands.command(help="Close a chatbot session.",aliases=["stop","terminate"])
  async def close(self, ctx):
    global inSesh
    if inSesh != None:
      pTalk.close()
      await ctx.send(f"Closed {inSesh}'s session, requested by {ctx.author}.", delete_after=db["del"])
      inSesh = None
    else:
      await ctx.send("No sessions active.", delete_after=db["del"])
def setup(bot):
    bot.add_cog(chatbot(bot))