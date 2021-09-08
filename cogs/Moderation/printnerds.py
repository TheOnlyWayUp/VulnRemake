import discord
from replit import db
from discord.ext import commands
from main import *

class printnerds(commands.Cog, name="Print nerds"):
  def __init__(self, bot):
      self.bot = bot
  @commands.command(help="Prints all users that haven't logged in in 3 days, are below level 20 and have got less than 21k gexp in the past 7 days.")
  async def printnerds(self, ctx, level:int=20, afk:int=2, xp:int=21000):
    if await stcheck(ctx) is True:
      resp = await req(f"https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2")
      members = resp["guild"]["members"]
      nerdl = commands.Paginator()
      for member in members:
        name = await returnName(member["uuid"])
        if True:
          trash = False
          reason = []
          try:
            if int(await returnLast(member["uuid"])) - current_time.day >= afk:
              trash = True
              reason.append(f"Hasn't logged in in {afk} days.")
          except Exception as e:
            #print(f"{e} at {returnName(member['uuid'])}, uuid = {member['uuid']}")
            pass
          
          try:
            if int(await functions.returnLevel(await returnName(member['uuid']))) < level:
              trash = True
              reason.append(f"Is below level {level}.")
          except Exception as e:
            #print(f"{e} at {returnName(member['uuid'])}, uuid = {member['uuid']}")
            pass
          try:
            xpHistory = []
            for key, value in member["expHistory"].items():
              xpHistory.append(value)
            if sum(xpHistory[-7:]) < xp:
              trash = True
              reason.append(f"Hasn't got {xp} gexp in the past 7 days.")
          except Exception as e:
            print(f"{e} at {await returnName(member['uuid'])}, uuid = {member['uuid']}")
          if trash is True:
            nerdl.add_line(f'{name} - {reason}')
          else:
            continue
        else:
          continue 
      for page in nerdl.pages:
        await ctx.send(page)
      await ctx.send("Completed!")
    else:
      await ctx.reply("You're not staff!")
def setup(bot):
    bot.add_cog(printnerds(bot))