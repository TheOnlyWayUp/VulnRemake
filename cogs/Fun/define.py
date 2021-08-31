import discord
from replit import db
from discord.ext import commands
from main import req
class define(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Finds the dictionary definition of a word")
  async def define(ctx, *, arg):
    try:
      word = await req(f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{arg}").json()[0]
      await ctx.send(f'Word - {word["word"]}\nDefinition - {word["meanings"][0]["definitions"][0]["definition"]}\nExamples - {word["meanings"][0]["definitions"][0]["example"]}', delete_after=db["del"])
    except:
      await ctx.send("There was an error finding this word.", delete_after=db["del"])
    await ctx.message.delete()
def setup(bot):
    bot.add_cog(define(bot))