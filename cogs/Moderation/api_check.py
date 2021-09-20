import discord, aiohttp, os
from replit import db
from main import stcheck
from discord.ext import commands

key_of_the_api = os.environ["api"]


class API_check(commands.Cog, name="API Check"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Checks if the API is functional.")
    @commands.check_any(commands.is_owner(), stcheck())
    async def api_check(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.hypixel.net/guild?key={key_of_the_api}&id=5e8c16788ea8c9ec75077ba2"
            ) as resp:
                x = await resp.json()
        if x["success"] is True:
            await ctx.reply(
                embed=discord.Embed(
                    title="Request successful.", color=discord.Colour.random()
                ),
                delete_after=db["del"],
            )
        elif x["success"] is False:
            await ctx.reply(
                f"Request failed, reason - {x['cause']}", delete_after=db["del"]
            )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(API_check(bot))
