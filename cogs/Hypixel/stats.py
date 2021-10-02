import discord, requests, shutil, os
from PIL import Image, ImageFont, ImageDraw
from replit import db
from discord.ext import commands
from main import *
import imgfunctions as functions
import io

statsclr = 0xFFFFFF


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Replies with the stats of the username given.")
    async def stats(self, ctx, ign):
        level = await functions.returnLevel(ign)
        uuid = await returnUUID(ign)
        name = await returnName(uuid)
        url = f"https://crafatar.com/renders/body/{uuid}"
        response = requests.get(url, stream=True)
        userdiscord = await returnDiscord(ign)
        with open("playerhead.png", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        im = Image.open("minecraft-aes1.gif")
        frames = []
        head = Image.open("playerhead.png")
        myFont = ImageFont.truetype("FreeMono.ttf", 35)
        myFontSize = ImageFont.truetype("FreeMono.ttf", 25)
        for frame in ImageSequence.Iterator(im):
            I1 = ImageDraw.Draw(frame)
            I1.text((26, 28), f"{name}'s Stats", font=myFont, fill=statsclr)
            I1.text((28, 70), f"Level - {level}", font=myFontSize, fill=statsclr)
            I1.text(
                (28, 100), f"Discord - {userdiscord}", font=myFontSize, fill=statsclr
            )
            I1.text(
                (28, 130),
                f"Guild - {await functions.returnGuild(ign)}",
                font=myFontSize,
                fill=statsclr,
            )
            im.paste(head, (376, 65), mask=head)
            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)
            frames.append(frame)
        frames[0].save("out.gif", save_all=True, append_images=frames)
        await ctx.send(file=discord.File("out.gif"))


def setup(bot):
    bot.add_cog(Stats(bot))
