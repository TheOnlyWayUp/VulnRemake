import discord, requests
from replit import db
from discord.ext import commands
from main import *


class getInfo(commands.Cog):
    """All the commands beginning with get, helps you get information.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Finds the Discord of a user, if paired through their Minecraft username."
    )
    async def getDiscord(self, ctx, ign):
        if await returnExistence(ign) is True:
            await ctx.reply(
                embed=discord.Embed(
                    title=str(await returnDiscord(ign)), color=discord.Colour.random()
                ),
                delete_after=db["del"],
            )
        else:
            await ctx.reply("That user isn't in the guild!", delete_after=db["del"])
        await ctx.message.delete()

    @commands.command(help="Checks if the user is in the guild.")
    async def getMS(self, ctx, ign):
        await ctx.reply(
            embed=discord.Embed(
                title=str(await returnMS(ign)), color=discord.Colour.random()
            ),
            delete_after=db["del"],
        )
        await ctx.message.delete()

    @commands.command(help="Gets the rank of a user in the guild.")
    async def getRank(self, ctx, ign):
        if await returnMS(ign) is True:
            await ctx.reply(
                embed=discord.Embed(
                    title=str(await returnRank(ign)), color=discord.Colour.random()
                ),
                delete_after=db["del"],
            )
        else:
            await ctx.reply("That user isn't in the guild!", delete_after=db["del"])
        await ctx.message.delete()

    @commands.command(
        help="Gets the top 10 players of the guild in terms of gexp contributions for the day."
    )
    async def getTop(self, ctx):
        data = requests.get(
            url="https://api.hypixel.net/guild",
            params={"key": {key_of_the_api}, "name": "Vuln"},
        ).json()
        embedStats = discord.Embed(
            title="Today's GTop",
            description="Today's top earning players.",
            color=0x6C9FCB,
        )
        playerDict = {}
        guild_stats = data["guild"]["members"]
        for item in guild_stats:
            total = sum(item["expHistory"].values())
            playerDict[item["uuid"]] = total
        playerDict = sorted(playerDict.items(), key=lambda x: -x[1])[:10]
        for x in range(10):
            embedStats.add_field(
                name=await returnName(playerDict[x][0]),
                value=f"{playerDict[x][1]} GExp",
                inline=False,
            )
        await ctx.send(embed=embedStats, delete_after=db["del"])
        await ctx.message.delete()

    @commands.command(help="Gets the UUID of a user.")
    async def getUUID(self, ctx, ign):
        await ctx.reply(
            embed=discord.Embed(
                title=str(await returnUUID(ign)), color=discord.Colour.random()
            ),
            delete_after=db["del"],
        )
        await ctx.message.delete()

    @commands.command(help="Gets the username of a user through their UUID.")
    async def getUsername(self, ctx, uuid):
        await ctx.reply(
            embed=discord.Embed(
                title=str(await returnName(uuid), color=discord.Colour.random())
            ),
            delete_after=db["del"],
        )
        await ctx.message.delete()

    @commands.command(help="Checks if a user is staff or helper.")
    @commands.check_any(commands.is_owner(), stcheck())
    async def getStaff(self, ctx):
        await ctx.reply(
            embed=discord.Embed(title="You're staff.", color=discord.Colour.random()),
            delete_after=db["del"],
        )

        await ctx.message.delete()

    @commands.command(help="A whois command")
    async def getWho(self, ctx, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = list(member.roles)
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            timestamp=ctx.message.created_at,
            title=f"User Info - {member}",
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(
            name="Created Account On:",
            value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
        )
        embed.add_field(
            name="Joined Server On:",
            value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
        )

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed, delete_after=db["del"])
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(getInfo(bot))
