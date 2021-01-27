import logging
import os
import subprocess

import requests
from discord import Embed, File
from discord.ext import commands

from config import *

upload_counter = 0
bot = commands.Bot(command_prefix='2x!')
logging.basicConfig(level=logLevel,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=".\log.txt",
                    filemode='w'
                    )

if cache_wipe_on_start:
    for f in os.listdir(cache_path):
        logging.info(f"Deleted {f} in {cache_path}.")
        os.remove(os.path.join(cache_path, f))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    logging.info(f"Logged in as {bot.user}, ID {bot.user.id}.")


@bot.command()
async def ping(ctx):
    print(ctx.author.id)
    await ctx.send(f"Pong! You are user {ctx.author}, or id {ctx.author.id}.")


@bot.command()
async def upscale(ctx):
    global upload_counter
    upload_counter += 1

    file_name = str(ctx.author.id) + "-" + str(upload_counter)

    logging.info(f"{ctx.author} ({ctx.author.id}) has uploaded the file {file_name} to {cache_path}.")

    msg_attachment_url = ctx.message.attachments[0].url
    req = requests.get(msg_attachment_url)
    with open(cache_path + "/{}.png".format(file_name), "xb") as attachment:
        attachment.write(req.content)

    w2x = subprocess.run(
        r"{} -v -i {} -o {} -n 2 -s 2 -g 0".format(w2x_exec_path, cache_path + r"/" + file_name + ".png",
                                                   cache_path + r"/" + file_name + "-O.png"),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    logging.info(w2x.stdout)

    upscaled_file = File(cache_path + r"/" + file_name + "-O.png", filename=file_name + "-O.png")
    embed = Embed()
    embed.set_image(url="attachment://{}".format(file_name + "-O.png"))
    await ctx.send(file=upscaled_file, embed=embed)


bot.run(token)
