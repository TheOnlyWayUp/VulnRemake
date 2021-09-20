from replit import db
from main import *
import discord
from discord.ext import commands


class staffRole(commands.Cog, name="Set staffrole"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Sets the staffrole.")
    async def staffRole(self, ctx, arg, rolement: discord.Role = 712458500940496936):
        if arg == "set":
            if (
                ctx.author.id == 562175882412687361
                or ctx.author.id == 876055467678375998
                or ctx.author.id == ctx.guild.owner.id
                or ctx.author.guild_permissions.administrator is True
            ):
                db["staffRole"] = rolement.name
                await ctx.send(f"I have set the staff role to {rolement}")
        elif arg == "view":
            await ctx.reply(f"The staff role is {db.get('staffRole')}")
        elif arg == "reset":
            if (
                ctx.author.id == 562175882412687361
                or ctx.author.id == ctx.guild.owner.id
                or ctx.author.guild_permissions.administrator is True
            ):
                db.set("staffRole", "")
                await ctx.reply("Reset the staff role.")

    @commands.command(help="Sets a user's nickname.")
    async def setNick(self, ctx, member: discord.Member = None, *, nick=None):
        if await stcheck(ctx) is True:
            await member.edit(nick=nick, reason=f"Run by {ctx.author.name}.")
            await ctx.reply("Done.", delete_after=db["del"])
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(staffRole(bot))
