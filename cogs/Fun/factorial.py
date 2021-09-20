import discord
from replit import db
from discord.ext import commands


def factorialcalc(n):
    if n == 0:
        return 1
    else:
        return n * factorialcalc(n - 1)


class factorial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Finds the factorial of a number")
    async def factorial(self, ctx, n: int):
        await ctx.reply(
            embed=discord.Embed(
                title=f"The factorial of {n} is {factorialcalc(n)}.",
                color=discord.Colour.random(),
            ),
            delete_after=db["del"],
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(factorial(bot))
