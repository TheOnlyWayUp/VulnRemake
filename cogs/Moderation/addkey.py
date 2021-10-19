import discord
from replit import db
from discord.ext import commands
from main import stcheck


class addkey(commands.Cog):
    """Contains the addkey and del_after commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Adds a key to the database.")
    @commands.check_any(commands.is_owner(), stcheck())
    async def add_key(self, ctx, key, *, value):
        """Adds a key and a value to the database, useful for modifying keys and testing.

        Args:
            ctx (contxt): Provided by system.
            key (string): The key to be added.
            value (string/int]): The value of the key.
        """
        if key != "del":
            db[key] = value
            await ctx.reply(
                embed=discord.Embed(
                    title=f"Set {key} to {value}", color=discord.Colour.random()
                ),
                delete_after=db["del"],
            )
        else:
            await ctx.reply("NAH, do v!delafter for that crap", delete_after=db["del"])
        await ctx.message.delete(delay=db["del"])

    @commands.command(help="Modifies the delete timer.")
    @commands.check_any(commands.is_owner(), stcheck())
    async def delafter(self, ctx, delf: int = 5):
        """Sets the delete after for messages.

        Args:
            ctx (contxt): Provided by system.
            delf (int, optional): The delete after value. Defaults to 5.
        """
        db["del"] = delf
        await ctx.reply(
            embed=discord.Embed(
                title=f"Set the del_after to {delf}.", color=discord.Colour.random()
            ),
            delete_after=db["del"],
        )
        await ctx.message.delete(delay=db["del"])

    @commands.command(help="Resets all database keys.")
    @commands.check_any(commands.is_owner(), stcheck())
    async def all_key_reset(self, ctx, confirm=False):
        if confirm is True:
            sg = await ctx.reply("**Resetting all keys...**")
            db["kickoffline"] = []
            db["noKickMsg"] = [889443874953646080, 889443132029157396]
            db["staffRole"] = "Helpers"
            db["del"] = 5
            await sg.edit("**Complete.**")


def setup(bot):
    bot.add_cog(addkey(bot))
