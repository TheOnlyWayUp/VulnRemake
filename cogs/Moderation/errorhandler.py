import discord
from discord.ext import commands
from replit import db

class ehandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
    message = "This is an undocumented error, it has been reported and will be patched in the next update."
    #raise error
    #Command not found
    if isinstance(error, commands.CommandNotFound):
      await ctx.message.add_reaction('⁉️')
      message = "Command not found."
    #On cooldown
    elif isinstance(error, commands.CommandOnCooldown):
      message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    #User doesn't have permissions
    elif isinstance(error, commands.MissingPermissions):
      message = "No permissions."
    elif isinstance(error, commands.BadArgument):
      message = "Bad arguement."
    #Not enough args
    elif isinstance(error, commands.UserInputError):
      message = f"Not all required arguements were passed, do `v!help {ctx.message.content[2:]}`"
    elif isinstance(error, commands.MissingRequiredArgument):
      message = f"Not all required arguements were passed, do `v!help {ctx.message.content[2:]}`"
    #Mentioned member not found
    elif isinstance(error, commands.MemberNotFound):
      message = "Couldn't find that member."
    #Bot doesn't have permissions
    elif isinstance(error.original, discord.errors.Forbidden):
      message = "Bot doesn't have the permissions needed."
    elif isinstance(error.original, discord.errors.Access):
      message = "Bot doesn't have the permissions needed."
    try:
      await ctx.send(embed=discord.Embed(title=message, color=0x992d22), delete_after=db["del"])
    except:
      await ctx.send(message, delete_after=db["del"])
    try:
      await ctx.message.delete()
    except:
      pass
def setup(bot):
  bot.add_cog(ehandler(bot))