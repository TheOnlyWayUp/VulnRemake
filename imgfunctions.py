
import requests
import math
import os
API_KEY = os.environ["api"]
async def returnUUID(ign=None):
  try:
    return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()["id"]
  except:
    return 404
BASE = 10_000
GROWTH = 2_500
REVERSE_PQ_PREFIX = -(BASE - 0.5 * GROWTH) / GROWTH
REVERSE_CONST = REVERSE_PQ_PREFIX
GROWTH_DIVIDES_2 = 2 / GROWTH
async def returnLevel(ign=None):
    data = requests.get(f"https://api.hypixel.net/player?key={API_KEY}&uuid={await returnUUID(ign)}").json()["player"]["networkExp"]
    if data is None:
        return 404
    return int(math.floor(1 + REVERSE_PQ_PREFIX + math.sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * int(data))))
async def returnGuild(ign=None):
  try:
    uuid = await returnUUID(ign)
    return requests.get(f"https://api.hypixel.net/guild?key={API_KEY}&player={uuid}").json()["guild"]["name"]
  except:
    return "N/A"