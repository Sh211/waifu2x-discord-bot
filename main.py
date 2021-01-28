import logging
import os
import subprocess
from sys import stdout

import requests
from discord import Embed, File
from discord.ext import commands

from config import *

upload_counter = 0
file_ext = None
bot = commands.Bot(command_prefix='2x!')  # Sets the bot's command prefix, so commands look like 2x!upscale
logging.basicConfig(level=logLevel,
                    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                    datefmt="%m-%d %H:%M",
                    filename=".\log.txt",
                    filemode="w"
                    )
rootLogger = logging.getLogger()
stdoutHandler = logging.StreamHandler(stdout)
stdoutHandler.setLevel(logLevel)
stdoutHandler.setFormatter(logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s"))
rootLogger.addHandler(stdoutHandler)


class InvalidFileTypeError(Exception):
    pass


if cache_wipe_on_start:
    for f in os.listdir(cache_path):
        logging.info(f"Deleted {f} in {cache_path}.")
        os.remove(os.path.join(cache_path, f))


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}, ID {bot.user.id}.")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! You are user {ctx.author}, or id {ctx.author.id}.")


@bot.command()
async def upscale(ctx):
    global upload_counter, file_ext
    upload_counter += 1

    file_name = str(ctx.author.id) + "-" + str(upload_counter)

    logging.info(f"{ctx.author} ({ctx.author.id}) has uploaded the file {file_name} to {cache_path}.")
    try:
        msg_attachment_url = ctx.message.attachments[0].url
        req = requests.get(msg_attachment_url)
        if msg_attachment_url.endswith(".png" or ".jpg"):
            file_ext = msg_attachment_url[-4:]
        elif msg_attachment_url.endswith(".jpeg" or ".mpeg"):
            file_ext = msg_attachment_url[-5:]
        else:
            raise InvalidFileTypeError

    except IndexError:
        await ctx.send(":x: | Please attach a picture to upscale.")
    except InvalidFileTypeError:
        await ctx.send(":x: | Attach a file of a supported type. (.png, .jpg, .mpeg)")
    else:
        with open(cache_path + f"/{file_name}{file_ext}", "xb") as attachment:
            attachment.write(req.content)

        w2x = subprocess.run(
            r"{} -v -i {} -o {} -n 2 -s 2 -g 0".format(w2x_exec_path, cache_path + r"/" + file_name + ".png", cache_path + r"/" + file_name + "-O.png"),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        logging.info(w2x.stdout)

        upscaled_file = File(cache_path + r"/" + file_name + f"-O{file_ext}", filename=file_name + f"-O{file_ext}")
        embed = Embed()
        embed.set_image(url="attachment://{}".format(file_name + f"-O{file_ext}"))
        await ctx.send(f":white_check_mark: | Here is your upscaled image, <@{ctx.author.id}>!", file=upscaled_file,
                       embed=embed)


bot.run(token)
