import discord
from replit import db
from discord.ext import commands
from main import *
class Rankgive(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Synchronises everyone's rank in the server to the ones in the guild.")
  async def rankgive(self, ctx):
    if await stcheck(ctx) is True:
      await ctx.reply("Processing.")
      await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game(name="synchronising roles..."))
      roles=[
      discord.utils.get(ctx.guild.roles, name="Guild member"),
      discord.utils.get(ctx.guild.roles, name="Active Guild Member"),
      discord.utils.get(ctx.guild.roles, name="Special Guild Member"),
    discord.utils.get(ctx.guild.roles, name="Helper")]
      ranks = ["Vulnerable","Active-Vuln","InVulnerable","Helpers","UnVulnerable"]
      users = [m for m in roles[0].members]
      changes = {"Updates":0,"Removals":0,"Errors":0,"Unknown":[]}
      async with ctx.typing():
        for user in users:
          username = user.display_name
          if await returnMS(username) is True:
            rank = await returnRank(username)
            #For normal guild members
            if rank == ranks[0]:
              await user.add_roles(roles[0], reason=f"v!rankgive by {ctx.author}")
              await user.remove_roles(roles[1], roles[2], roles[3])
            #For active users
            elif rank == ranks[1]:
              await user.add_roles(roles[0], roles[1], reason=f"v!rankgive by {ctx.author}")
              await user.remove_roles(roles[2], roles[3])
            #For inv/unvulnerables
            elif rank == ranks[2] or rank == ranks[4]:
              await user.add_roles(roles[0], roles[2], reason=f"v!rankgive by {ctx.author}")
              await user.remove_roles(roles[1], roles[3])
            #For helpers
            elif rank == ranks[3]:
              await user.add_roles(roles[0], roles[3], reason=f"v!rankgive by {ctx.author}")
              await user.remove_roles(roles[1], roles[2])
            else:
              changes["Unknown"].append({username:rank})
              changes["Errors"] += 1
            changes["Updates"] += 1
          elif await returnMS(username) is False:
            await user.remove_roles(roles[0], roles[1], roles[2], roles[3])
            changes["Removals"] += 1
          else:
            changes["Errors"] += 1
            continue
      #Back to normal indentation
      rngEmbed = discord.Embed(title="Rankgive successful",color=0x70e7a4)
      for key in changes.keys():
        if key != "Unknown":
          rngEmbed.add_field(name=key, value=changes[key], inline=False)
        else:
          unkstr=""
          for item in changes["Unknown"]:
            unkstr = unkstr + "\n" + str(item)
          rngEmbed.add_field(name=key, value=unkstr, inline=False)
      await asyncio.sleep(5)
      await ctx.reply(embed=rngEmbed)
      await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.listening, name="v!help and mentions."))
def setup(bot):
  bot.add_cog(Rankgive(bot))
