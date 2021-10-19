import discord, aiohttp, os
from replit import db
from main import stcheck
from discord.ext import commands

key_of_the_api = os.environ["api"]


class API_check(commands.Cog, name="API Check"):
    """API_check contains database and API checks that make can tell if you anything is amiss.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Checks if the API is functional.")
    @commands.check_any(commands.is_owner(), stcheck())
    async def api_check(self, ctx):
        """Checks if the API is functional.

        Args:
            ctx (context): Provided by system. 
        """
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
        await ctx.message.delete(delay=db["del"])

    @commands.command(help="Checks if the database is functional.")
    @commands.check_any(commands.is_owner(), stcheck())
    async def db_check(self, ctx):
        """Checks if the database is functional by creating a key with the user.id and deleting it.

        Args:
            ctx (context): Provided by system.
        """
        try:
            db[str(ctx.author.id)] = "Vuln Gang"
            del db[str(ctx.author.id)]
            await ctx.reply(
                embed=discord.Embed(
                    title="Request successful.", color=discord.Colour.random()
                ),
                delete_after=db["del"],
            )
        except Exception as e:
            await ctx.reply(f"Request failed, reason - {e}", delete_after=db["del"])
        await ctx.message.delete(delay=db["del"])


def setup(bot):
    bot.add_cog(API_check(bot))
