import discord
from replit import db
from discord.ext import commands
from main import bot


class Exec(commands.Cog):
    """Allows bot supervisor accounts to run code in console.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Executes the given arguement as python.", hidden=True)
    async def exec(self, ctx, *, to_exec):
        if ctx.author.id == 876055467678375998:
            try:
                exec(to_exec)
                await ctx.reply("Done.")
            except Exception as e:
                await ctx.reply(
                    f"There was an error - {e}", delete_after=db["del"] * 1.5
                )


def setup(bot):
    bot.add_cog(Exec(bot))
