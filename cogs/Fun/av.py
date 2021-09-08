import discord, random, string, aiohttp
from replit import db
from discord.ext import commands
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from main import req
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
  @commands.command(help="Generates a random default avatar for the user with or without a provided seed.")
  async def genav(self, ctx, seed=None):
      try:
        if seed is None:
          seed = random.sample(string.ascii_letters, 5)
        async with aiohttp.ClientSession() as session:
          async with session.get(f"https://avatars.dicebear.com/api/micah/{seed}.svg?mood[]=happy") as resp:
            img_data = await resp.content.read()
        with open('img.svg', 'wb') as handler:
          handler.write(img_data)
        drawing = svg2rlg('img.svg')
        renderPM.drawToFile(drawing, 'img2.png', fmt='PNG')
        with open("img2.png", "rb") as fh:
          f = discord.File(fh, filename="av.png")
        await ctx.reply(file=f, delete_after=db["del"])
        await ctx.message.delete()
      except:
        pass
def setup(bot):
  bot.add_cog(getAv(bot))