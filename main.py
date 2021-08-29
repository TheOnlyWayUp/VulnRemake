#Import libraries
import discord, aiohttp, asyncio, os, datetime
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp
#Import info from .env file
key_of_the_api = os.environ["api"]
token = os.environ["token"]
#Init the bot class
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(commands.when_mentioned_or("v!","V!","vuln!","Vuln!"),intents=intents,activity=discord.Activity(type=discord.ActivityType.listening,name="v!help or mentions!"), case_insensitive=True)
menu = DefaultMenu(page_left="⬅", page_right="➡", remove="❌", active_time=5)
bot.help_command = PrettyHelp(menu=menu, ending_note="Run by {ctx.author.name}", index_title="**VULN**", no_category="**VULN**", sort_commands=True)
all_categories = [category for category in os.listdir("./cogs")]
print(all_categories)
for category in all_categories:
  for filename in os.listdir(f"./cogs/{category}"):
      if filename.endswith(".py"):
        bot.load_extension(f"cogs.{category}.{filename[:-3]}")
        print(f"Succesfully Loaded Cog: {filename}")
      else:
        continue
#Main functions
async def req(link):
  async with aiohttp.ClientSession() as session:
    async with session.get(link) as resp:
      return await resp.json()
async def returnUUID(ign=None):
  resp = await req(f"https://api.mojang.com/users/profiles/minecraft/{ign}")
  return resp["id"]
async def returnName(uuid=None):
  resp = await req(f"https://api.mojang.com/users/profiles/minecraft/{uuid}")
  return resp["name"]
async def returnLast(check=None, ty="name"):
  if ty == "name":
    check = await returnUUID(check)
  elif ty == "uuid":
    check = check
  last = await req(f'https://api.hypixel.net/player?key={key_of_the_api}&uuid={check}')
  return datetime.datetime.utcfromtimestamp(int(last["player"]["lastLogin"])/1000).strftime('%d')
async def returnExistence(check=None, ty="name"):
  if ty == "name":
    try:
      await req(f"https://api.mojang.com/users/profiles/minecraft/{check}")
      return True
    except:
      return False
async def returnDiscord(check=None, ty="name"):
  if ty == "name":
    check = await returnUUID(check)
  elif ty == "uuid":
    check = check
  return req(f"https://api.hypixel.net/player?key={key_of_the_api}&uuid={check}")["player"]["socialMedia"]["links"]["DISCORD"]
async def returnMS(check=None, ty="name"):
  members = await req(f'https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2')["guild"]["members"]
  if ty == "name":
    check = returnUUID(check)
  elif ty == "uuid":
    check = check
  for member in members:
    if check == member["uuid"]:
      return True
    else:
      continue
  return False
async def returnRank(check=None, ty="name"):
  members = await req(f'https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2')["guild"]["members"]
  if ty == "name":
    check = await returnUUID(check)
  elif ty == "uuid":
    check = check
  for member in members:
    if member["uuid"] == check:
      return member["rank"]



#bot.run(token)

