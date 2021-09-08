import discord, prsaw2
from replit import db
from discord.ext import commands
pTalk = prsaw2.Client(key='Yfbjgiz58BIR')
from main import req
class Chatbot(commands.Cog):
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
    await ctx.message.delete()
  @commands.command(help="Close a chatbot session.",aliases=["stop","terminate"])
  async def close(self, ctx):
    global inSesh
    if inSesh != None:
      pTalk.close()
      await ctx.send(f"Closed {inSesh}'s session, requested by {ctx.author}.", delete_after=db["del"])
      inSesh = None
    else:
      await ctx.send("No sessions active.", delete_after=db["del"])
    await ctx.message.delete()
  @commands.command(help="Sends a (pretty trash) joke.")
  async def joke(self, ctx):
    pJoke = prsaw2.Client(key='Yfbjgiz58BIR')
    jokebruh = pJoke.get_joke(type="any").joke
    jokeson = jokebruh
    try:
      if "setup" in jokeson.keys():
        jem = discord.Embed(title=jokeson["setup"], description=jokeson["delivery"], color=discord.Colour.random())
        await ctx.send(embed=jem, delete_after=db["del"])
    except:
      jem = discord.Embed(title=jokebruh, color=discord.Colour.random())
      await ctx.send(embed=jem, delete_after=db["del"])
    pJoke.close()
    await ctx.message.delete()
  @commands.command(help="Sends a meme.")
  async def meme(self, ctx):
    data = await req("https://meme-api.herokuapp.com/gimme")
    if data["nsfw"] is False:
      meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    else:
      await ctx.reply("Please run the command again.", delete_after=db["del"])
    await ctx.reply(embed=meme, delete_after=db["del"])
    await ctx.message.delete()
def setup(bot):
    bot.add_cog(Chatbot(bot))