import discord
from replit import db
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Pings the bot and returns latency.")
    async def ping(self, ctx):
        pem = discord.Embed(
            title="Pong!",
            description=f"Your ping is {round(self.bot.latency * 1000)}ms.",
            color=0x39F220,
        )
        pem.set_footer(
            text="Version 1.3.5 of the VULN Bot. Created by TheOnlyWayUp#1231."
        )
        await ctx.reply(embed=pem, delete_after=db["del"])
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Ping(bot))
