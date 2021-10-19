import discord
from discord_components import *
from discord.ext import commands
from replit import db
from main import stcheck, bot


class Reload(commands.Cog, name="Reload/Load commands"):
    """I don't think this shit even works lol
    """
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(self.bot)

    @commands.Cog.listener()
    async def on_button_click(function, interaction):
        arg = interaction.component.custom_id
        rl = interaction.message.content[31:]
        # await interaction.respond(content=f'Trying to {arg} {interaction.message.content[31:]}')
        if arg == "reload":
            try:
                bot.reload_extension(rl)
                await interaction.respond(content="Done.")
            except Exception as e:
                await interaction.respond(content=f"Error - {e}.")
        elif arg == "unload":
            try:
                bot.unload_extension(rl)
                await interaction.respond(content="Done.")
            except Exception as e:
                await interaction.respond(content=f"Error - {e}.")
        elif arg == "load":
            try:
                bot.load_extension(rl)
                await interaction.respond(content="Done.")
            except Exception as e:
                await interaction.respond(content=f"Error - {e}.")
        elif arg == "newload":
            try:
                self.bot.load_extension(rl)
                bot.reload_extension(rl)
                await interaction.respond(content="Done.")
            except Exception as e:
                await interaction.respond(content=f"Error - {e}.")

    @commands.command(help="Reloads/Loads a new cog or file.", hidden=True)
    @commands.check_any(commands.is_owner(), stcheck())
    async def load(self, ctx, arg):
        await ctx.reply(
            f"What would you like to do to - {arg}",
            components=[
                [
                    Button(label="Reload", custom_id="reload", style=1),
                    Button(label="Load", custom_id="load", style=1),
                    Button(label="Unload", custom_id="unload", style=1),
                    Button(label="Newload", custom_id="newload", style=1),
                ]
            ],
            delete_after=db["del"] * 2,
        )
        # interaction = await self.bot.wait_for("button_click", check = lambda i: i.custom_id  == "reload")
        # await interaction.send(content = "Button clicked!")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Reload(bot))
