import discord
from discord.ext import commands
from replit import db
from main import *


class ehandler(commands.Cog):
    """The main error handler.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """Error handler.

        Args:
            ctx (commands.Context): Provided by system.
            error (commands.CommandError): The error object.

        Raises:
            error: Raises error if undocumented.
        """

        # raise error
        # Command not found
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("⁉️")
            message = "Command not found."
        # On cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("❌")
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        # User doesn't have permissions
        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction("🔐")
            message = "No permissions."
        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction("🤏")
            message = "Bad arguement."
        # Not enough args
        elif isinstance(error, commands.UserInputError):
            await ctx.message.add_reaction("🤏")
            message = f"Not all required arguements were passed, do `v!help {ctx.message.content[2:]}`"
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("🤏")
            message = f"Not all required arguements were passed, do `v!help {ctx.message.content[2:]}`"
        # Mentioned member not found
        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.add_reaction("🤷‍♂️")
            message = "Couldn't find that member."
        # Bot doesn't have permissions
        elif isinstance(error.original, discord.errors.Forbidden):
            await ctx.message.add_reaction("📛")
            message = "Bot doesn't have the permissions needed."
        else:
            message = "This is an undocumented error, it has been reported and will be patched in the next update."
            raise error
        try:
            await ctx.send(
                embed=discord.Embed(title=message, color=0x992D22),
                delete_after=db["del"],
            )
        except:
            await ctx.send(message, delete_after=db["del"])
        try:
            await ctx.message.delete(delay=db["del"])
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """DMs user asking for their username on join.
        """
        guild = member.guild

        def check(m: discord.Message):
            return m.author.id == member.id and isinstance(
                m.channel, discord.channel.DMChannel
            )

        mem = discord.Embed(
            title=f"Welcome to Vuln, {member.name}!",
            description=f"Type your username.",
            color=0x39F220,
        )
        await member.send(embed=mem)
        user = await self.bot.wait_for(event="message", check=check, timeout=30)
        if await returnExistence(user) is True:
            dcRole = discord.utils.get(guild.roles, name="Discord Member")
            try:
                disc = await returnDiscord(user.content)
            except:
                await user.reply(
                    "You aren't linked to Hypixel.\nTutorial - <https://hypixel.net/threads/guide-how-to-link-discord-account.3315476/>",
                    mention_author=False,
                )
                return
            ranks = ["Vulnerable", "Active-Vuln", "InVulnerable", "Helpers"]
            rank = await returnRank(user.content)
            roles = [
                discord.utils.get(guild.roles, name="Guild member"),
                discord.utils.get(guild.roles, name="Active Guild Member"),
                discord.utils.get(guild.roles, name="Special Guild Member"),
                discord.utils.get(guild.roles, name="Helper"),
            ]
            if str(disc) == str(user.author):
                if rank == ranks[0]:
                    await member.add_roles(roles[0], reason=f"v!pair by {user.author}")
                    await member.author.remove_roles(roles[1], roles[2], roles[3])
                if rank == ranks[1]:
                    await member.add_roles(
                        roles[0], roles[1], reason=f"v!pair by {user.author}"
                    )
                    await member.remove_roles(roles[2], roles[3])
                if rank == ranks[2]:
                    await member.add_roles(
                        roles[0], roles[2], reason=f"v!pair by {user.author}"
                    )
                    await member.remove_roles(roles[1], roles[3])
                if rank == ranks[3]:
                    await member.add_roles(
                        roles[0], roles[3], reason=f"v!pair by {user.author}"
                    )
                    await member.remove_roles(roles[1], roles[2])
                try:
                    await member.edit(nick=user.content)
                    await user.reply(
                        embed=discord.Embed(
                            title=f"Successfuly paired to {user.content}!",
                            color=0x70E7A4,
                        ),
                        delete_after=db["del"],
                    )
                except Exception as e:
                    print(e)
                    await user.reply(
                        embed=discord.Embed(
                            title=f"Successfuly paired to {user.content} but unable to set nickname.",
                            color=0xFFEA9B,
                        ),
                        mention_author=False,
                        delete_after=db["del"],
                    )
            else:
                await user.reply(
                    embed=discord.Embed(
                        title=f"Pairing failed. Check the account you have paired to Minecraft. Different fonts/tags are not supported.",
                        color=0xEA5852,
                    ),
                    mention_author=False,
                    delete_after=db["del"],
                )
                await user.reply(
                    "Tutorial - <https://hypixel.net/threads/guide-how-to-link-discord-account.3315476/>",
                    mention_author=False,
                    delete_after=db["del"],
                )
        else:
            await user.reply(
                "That Minecraft account doesn't exist!", delete_after=db["del"]
            )
        # await ign.reply(ign.content)
        await guild.system_channel.send(f"Welcome to Vuln, {member.name}.")


def setup(bot):
    bot.add_cog(ehandler(bot))
