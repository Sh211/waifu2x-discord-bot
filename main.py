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
#  Logging setup
bot = commands.Bot(command_prefix='2x!')  # Sets the bot's command prefix, so commands look like 2x!upscale
logging.basicConfig(level=logLevel,
                    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                    datefmt="%m-%d %H:%M",
                    filename=".\log.txt",
                    filemode="w"
                    ) 
#  The block of code below makes the logger output to STDOUT aswell
rootLogger = logging.getLogger()
stdoutHandler = logging.StreamHandler(stdout)
stdoutHandler.setLevel(logLevel)
stdoutHandler.setFormatter(logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s"))
rootLogger.addHandler(stdoutHandler)


class InvalidFileTypeError(Exception):
    pass

#  Delete all files in the cache if the variable cache_wipe_on_start is True (and logs it)
if cache_wipe_on_start:
    for f in os.listdir(cache_path):
        logging.info(f"Deleted {f} in {cache_path}.")
        os.remove(os.path.join(cache_path, f))

#  Sends a logged notification that the bot is ready to execute commands
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
    
    #  Detect the uploaded file format - waifu2x supports .png, .jpg and .mpeg only 
    try:
        msg_attachment_url = ctx.message.attachments[0].url
        req = requests.get(msg_attachment_url)
        if msg_attachment_url.endswith(".png" or ".jpg"):
            file_ext = msg_attachment_url[-4:]
        elif msg_attachment_url.endswith(".jpeg" or ".mpeg"):
            file_ext = msg_attachment_url[-5:]
        else:
            raise InvalidFileTypeError
            
    except IndexError: #  IndexError only occurs when there is no attachment
        await ctx.send(":x: | Please attach a picture to upscale.")
        
    except InvalidFileTypeError: #  Use the custom exception we made (for clarity) to notify of an invalid file type
        await ctx.send(":x: | Attach a file of a supported type. (.png, .jpg, .mpeg)")
        
    else:
        #  Download the file into the cache
        with open(cache_path + f"/{file_name}{file_ext}", "xb") as attachment:
            attachment.write(req.content)
            
        #  This mess of args and etc runs your installation of waifu2x on the downloaded image and outputs a file that is scaled up
        #  to a scale of two, a noise-reduction level of two, and using GPU 0.
        w2x = subprocess.run(
            r"{} -v -i {} -o {} -n 2 -s 2 -g 0".format(w2x_exec_path, cache_path + r"/" + file_name + ".png", cache_path + r"/" + file_name + "-O.png"),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        #  Also logs the output of waifu2x.
        logging.info(w2x.stdout)
        
        #  Send the file back to the user, pinging them in the process. Discord is a *little* tricky, so we have to use an embed here.
        upscaled_file = File(cache_path + r"/" + file_name + f"-O{file_ext}", filename=file_name + f"-O{file_ext}")
        embed = Embed()
        embed.set_image(url="attachment://{}".format(file_name + f"-O{file_ext}"))
        await ctx.send(f":white_check_mark: | Here is your upscaled image, <@{ctx.author.id}>!", file=upscaled_file,
                       embed=embed)


bot.run(token)
