import discord
from discord.ext import commands

class KickOffline(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.role_message_id = 886657801013854228
      self.emoji_to_role = [discord.PartialEmoji(name='🔴')]

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        print(f"{payload.member} reacted with {payload.emoji}")

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

def setup(bot):
  bot.add_cog(KickOffline(bot))