import discord, aiohttp
from replit import db
from discord.ext import commands
from main import *

class pair(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Lets a user pair with their MC account.")
  async def pair(self, ctx, user=None):
    if await returnExistence(user) is True:
      #dcRole = discord.utils.get(ctx.guild.roles, name="Discord Member")
      disc = await returnDiscord(user)
      pairing(user, disc, ctx.author)
      ranks = ["Vulnerable","Active-Vuln","InVulnerable","Helpers"]
      rank = await returnRank(user)  
      roles=[
  discord.utils.get(ctx.guild.roles, name="Guild member"),
  discord.utils.get(ctx.guild.roles, name="Active Guild Member"),
  discord.utils.get(ctx.guild.roles, name="Special Guild Member"),
discord.utils.get(ctx.guild.roles, name="Helper")]
      if str(disc) == str(ctx.author):
        if rank == ranks[0]:
          await ctx.author.add_roles(roles[0], reason=f"v!pair by {ctx.author}")
          await ctx.author.remove_roles(roles[1], roles[2], roles[3])
        if rank == ranks[1]:
          await ctx.author.add_roles(roles[0], roles[1], reason=f"v!pair by {ctx.author}")
          await ctx.author.remove_roles(roles[2], roles[3])
        if rank == ranks[2]:
          await ctx.author.add_roles(roles[0], roles[2], reason=f"v!pair by {ctx.author}")
          await ctx.author.remove_roles(roles[1], roles[3])
        if rank == ranks[3]:
          await ctx.author.add_roles(roles[0], roles[3], reason=f"v!pair by {ctx.author}")
          await ctx.author.remove_roles(roles[1], roles[2])
        try:
          await ctx.author.edit(nick=user)
          await ctx.send(embed=discord.Embed(title=f"Successfuly paired to {user}!", color=0x70e7a4), delete_after=db["del"])
        except Exception as e:
          print(e)
          await ctx.reply(embed=discord.Embed(title=f"Successfuly paired to {user} but unable to set nickname.", color=0xffea9b), mention_author=False, delete_after=db["del"])
      else:
        await ctx.reply(embed=discord.Embed(title=f"Pairing failed. Check the account you have paired to Minecraft. Different fonts/tags are not supported.", color=0xea5852), mention_author=False,delete_after=db["del"])
        await ctx.reply("Tutorial - <https://hypixel.net/threads/guide-how-to-link-discord-account.3315476/>", mention_author=False,delete_after=db["del"])
    else:
      await ctx.send("That Minecraft account doesn't exist!",delete_after=db["del"])

def setup(bot):
    bot.add_cog(pair(bot))