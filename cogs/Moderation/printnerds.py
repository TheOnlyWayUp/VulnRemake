import discord
from replit import db
from discord.ext import commands
from discord_components import *
from main import *
import datetime
class printnerds(commands.Cog, name="Print nerds"):
  def __init__(self, bot):
      self.bot = bot
      DiscordComponents(self.bot)
  @commands.command(help="Prints all users that haven't logged in in 3 days, are below level 20 and have got less than 21k gexp in the past 7 days.")
  async def printnerds(self, ctx, level:int=20, afk:int=2, xp:int=21000):
    if await stcheck(ctx) is True:
      current_time = datetime.datetime.now() 
      await ctx.reply("Processing...", delete_after=db["del"])
      async with ctx.typing():
        notnerds = []
        for item in db["kickoffline"]:
          notnerds.append(item["Name"])
        resp = await req(f"https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2")
        members = resp["guild"]["members"]
        nerdl = commands.Paginator()
        for member in members:
          name = await returnName(member["uuid"])
          cont = True
          for notname in notnerds:
            if notname == name:
              cont = False
          if cont is True:
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
    
  @commands.command(help="Kicklist related commands.")
  async def kicklist(self, ctx, ign=None, reason=None, length=None, remove=False):
    if await stcheck(ctx) is True:
      if ign is None:
        await ctx.reply(f"What would you like to do to?", components = [[Button(label = "Reset", custom_id = "reset", style=1),Button(label = "View", custom_id = "view", style=1)]], delete_after=db["del"]*1)
      elif ign is not None:
        if await returnMS(ign) is True:
          if remove is False:
            current_time = datetime.datetime.now()
            db["kickoffline"].append({"Name":ign, "Reason":reason, "Length":length, "Start":f"{current_time.day}/{current_time.month}"})
            await ctx.reply(f"Added {ign} to the no-kicklist.", delete_after=db["del"])
          else:
            for item in db["kickoffline"]:
              if ign.lower() == item["Name"].lower():
                db["kickoffline"].remove(item)
                await ctx.reply("Done.", delete_after=db["del"])
                break
              else:
                continue
              await ctx.reply("Not found.", delete_after=db["del"])
    await ctx.message.delete()
  @commands.command(help="The most retarded command in existence.")
  async def kickoffline1992(self, ctx, arg=None):
    if await stcheck(ctx) is True:
      if arg == "reset":
        db["kickoffline"] = []
        await ctx.reply("Done.", delete_after=db["del"])
    await ctx.message.delete()


  @commands.Cog.listener()
  async def on_button_click(function, interaction):
    arg = interaction.component.custom_id
    if arg == "reset":
      await interaction.respond(content="Do `v!kickoffline1992 reset`.")
    elif arg == "view":
      kembed = discord.Embed(title="The no kicklist.", color=discord.Color.random())
      for item in db["kickoffline"]:
        kembed.add_field(name=item["Name"], value=f"Reason - {item['Reason']}\nStart time - {item['Start']}\nLength - {item['Length']} days.")
      await interaction.respond(embed=kembed)
  
  

def setup(bot):
    bot.add_cog(printnerds(bot))