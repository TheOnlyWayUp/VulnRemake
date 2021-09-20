import discord, requests
from replit import db
from discord.ext import commands
from main import req


class define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Finds the dictionary definition of a word")
    async def define(self, ctx, *, arg):
        try:
            word = await req(
                f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{arg}"
            )
            word = word[0]
            await ctx.reply(
                embed=discord.Embed(
                    title=word["word"],
                    description=f'Definition - {word["meanings"][0]["definitions"][0]["definition"]}\nExamples - {word["meanings"][0]["definitions"][0]["example"]}',
                    color=discord.Colour.random(),
                ),
                delete_after=db["del"],
            )
        except:
            await ctx.send(
                "There was an error finding this word.", delete_after=db["del"]
            )
        await ctx.message.delete()

    @commands.command(help="Finds the top urban dictionary definition of a word.")
    async def ud(self, ctx, *, word):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": word}
        headers = {
            "x-rapidapi-key": "284d301836msh3bcccd73d2de2a4p106e55jsnb38c121f66a0",
            "x-rapidapi-host": "mashape-community-urban-dictionary.p.rapidapi.com",
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        await ctx.reply(
            embed=discord.Embed(
                title=word,
                description=f'{response.json()["list"][0]["definition"]}\n\nExamples -\n{response.json()["list"][0]["example"]}',
                color=discord.Colour.random(),
            ),
            delete_after=db["del"],
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(define(bot))
