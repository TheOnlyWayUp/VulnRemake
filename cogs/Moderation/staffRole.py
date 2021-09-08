from replit import db
from main import *
import discord
from discord.ext import commands

class staffRole(commands.Cog, name="Set staffrole"):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(help="Sets the staffrole.")
  async def staffRole(self, ctx, arg, rolement: discord.Role=884480740421672991):
    if arg == "set" and ctx.author.id == 562175882412687361 or ctx.author.id == ctx.guild.owner.id or ctx.author.guild_permissions.administrator is True:
      db["staffRole"] = rolement.name
      await ctx.send(f"I have set the staff role to {rolement}")
    elif arg=="view":
      await ctx.reply(f"The staff role is {await db.get('staffRole')}")
    elif arg == "reset" and ctx.author.id == 562175882412687361 or ctx.author.id == ctx.guild.owner.id or ctx.author.guild_permissions.administrator is True:
      await db.set("staffRole","")
      await ctx.reply("Reset the staff role.")

def setup(bot):
    bot.add_cog(staffRole(bot))