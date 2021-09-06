import discord
from replit import db
from discord.ext import commands
from main import *

class forcepair(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Forcepairs a user, does not authenticate if the user mentioned owns the Minecraft account.")
  async def forcepair(self, ctx, member: discord.Member,user=None):
    if await stcheck(ctx) is True:
      disc = await returnDiscord(user)
      rank = await returnRank(user)
      ranks = ["Vulnerable","Active-Vuln","InVulnerable","Helpers","UnVulnerable"]
      roles=[discord.utils.get(ctx.guild.roles, name="Guild member"),discord.utils.get(ctx.guild.roles, name="Active Guild Member"),discord.utils.get(ctx.guild.roles, name="Special Guild Member"),discord.utils.get(ctx.guild.roles, name="Helper")]  
      try:
        if rank == ranks[0]:
          await member.add_roles(roles[0], reason=f"v!pair by {ctx.author}")
          await member.remove_roles(roles[1], roles[2], roles[3])
        if rank == ranks[1]:
          await member.add_roles(roles[0], roles[1], reason=f"v!pair by {ctx.author}")
          await member.remove_roles(roles[2], roles[3])
        if rank == ranks[2] or await returnRank(user) == ranks[4]:
          await member.add_roles(roles[0], roles[2], reason=f"v!pair by {ctx.author}")
          await member.remove_roles(roles[1], roles[3])
        if rank == ranks[3]:
          await member.add_roles(roles[0], roles[3], reason=f"v!pair by {ctx.author}")
          await member.remove_roles(roles[1], roles[2])
        try:
          await member.edit(nick=user)
          await ctx.send(embed=discord.Embed(title=f"Successfuly paired to {user}!", color=0x70e7a4), delete_after=db["del"])
        except Exception as e:
          print(e)
          await ctx.reply(embed=discord.Embed(title=f"Successfuly paired to {user} but unable to set nickname.", color=0xffea9b), mention_author=False, delete_after=db["del"])
      except:
        await ctx.reply(embed=discord.Embed(title=f"Pairing failed. Check the account you have paired to Minecraft. Different fonts/tags are not supported.", color=0xea5852), mention_author=False,delete_after=db["del"])
        await ctx.reply("Tutorial - <https://hypixel.net/threads/guide-how-to-link-discord-account.3315476/>", mention_author=False,delete_after=db["del"])
    else:
      await ctx.send("You gotto be staff for that.")
  
def setup(bot):
    bot.add_cog(forcepair(bot))