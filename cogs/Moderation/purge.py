import discord
from replit import db
from discord.ext import commands
from main import stcheck


class purge(commands.Cog, name="Purge"):
    """Purge command.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Purges a given number of messages, defaults to 15")
    @commands.cooldown(rate=1, per=3)
    @commands.check_any(commands.is_owner(), stcheck())
    async def purge(self, ctx, amount=30):
        """Purges x amount of deleted messages in current channel.

        Args:
            ctx (Context): Provided by system.
            amount (int, optional): Number of messages to purge. Defaults to 30.
        """
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=amount + 1):
            messages.append(message)
        await channel.delete_messages(messages)
        await ctx.send(
            embed=discord.Embed(
                title=f"{amount} messages have been purged by {ctx.message.author.name}",
                color=discord.Colour.random(),
            ),
            delete_after=db["del"],
        )
        await ctx.message.delete(delay=db["del"])


def setup(bot):
    bot.add_cog(purge(bot))
