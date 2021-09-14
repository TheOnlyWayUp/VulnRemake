#Import libraries
import discord, aiohttp, asyncio, os, datetime
from termcolor import cprint
from replit import db
from discord.ext import commands
from better_help import Help
#from pretty_help import DefaultMenu, PrettyHelp
#Import info from .env file
key_of_the_api = os.environ["api"]
token = os.environ["token"]
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#Init the bot class
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(
  commands.when_mentioned_or("v!","V!","vuln!","Vuln!"),intents=intents,case_insensitive=True,help_command=Help())
'''
menu = DefaultMenu(page_left="⬅", page_right="➡", remove="❌", active_time=5)
bot.help_command = PrettyHelp(menu=menu, ending_note="Run by {ctx.author.name}", index_title="**VULN**", no_category="**VULN**", sort_commands=True)
'''
all_categories = [category for category in os.listdir("./cogs")]

#Main functions
async def req(link):
  async with aiohttp.ClientSession() as session:
    async with session.get(link) as resp:
      return await resp.json()
async def returnUUID(ign=None):
  try:
    resp = await req(f"https://api.mojang.com/users/profiles/minecraft/{ign}")
    return resp["id"]
  except:
    return "404"
async def returnName(uuid=None):
  try:
    resp = await req(f"https://api.mojang.com/user/profile/{uuid}")
    return resp["name"]
  except:
    return uuid
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
  x= await req(f"https://api.hypixel.net/player?key={key_of_the_api}&uuid={check}")
  try:
    return x["player"]["socialMedia"]["links"]["DISCORD"]
  except:
    return "unpaired"
async def returnMS(check=None, ty="name"):
  members = await req(f'https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2')
  if ty == "name":
    check = await returnUUID(check)
  elif ty == "uuid":
    check = check
  for member in members["guild"]["members"]:
    if check == member["uuid"]:
      return True
    else:
      continue
  return False
async def returnRank(check=None, ty="name"):
  members = await req(f'https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2')
  if ty == "name":
    check = await returnUUID(check)
  elif ty == "uuid":
    check = check
  for member in members["guild"]["members"]:
    if member["uuid"] == check:
      return member["rank"]
  return "not in guild"
#Return staff status of a user
async def stcheck(ctx):
    role = discord.utils.get(ctx.guild.members, name=db["staffRole"])
    roleasd = discord.utils.find(lambda r: r.name == "God Father", ctx.message.guild.roles)
    if role in ctx.author.roles or str(ctx.author.id) == str(ctx.guild.owner.id) or roleasd in ctx.author.roles or ctx.author.guild_permissions.administrator is True or str(ctx.author.id) == str(562175882412687361) or str(ctx.author.id) == str(876055467678375998):
      return True
    else:
      return False


#Loading cogs
print(all_categories)
for category in all_categories:
  for filename in os.listdir(f"./cogs/{category}"):
      if filename.endswith(".py"):
        try:
          bot.load_extension(f"cogs.{category}.{filename[:-3]}")
          cprint(f"Loaded {filename}", "green")
        except Exception as e:
          cprint(f"Unable to load {filename} due to {e}", "red")
          continue
      else:
        continue



@bot.event
async def on_ready():
  print("Ready.")
  await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.listening, name="v!help and mentions."))

bot.run(token)

