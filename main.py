import logging
import requests
from config import *
from discord.ext import commands

upload_counter = 0
bot = commands.Bot(command_prefix='2x!')
logging.basicConfig(level=logLevel,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=attachment_cache_path + "\log.txt",
                    filemode='w'
                    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    logging.info(f"Logged in as {bot.user}, ID {bot.user.id}.")


@bot.command()
async def ping(ctx):
    print(ctx.author.id)
    await ctx.send(f"Pong! You are user {ctx.author}, or id {ctx.author.id}.")


@bot.command()
async def upload(ctx):
    global upload_counter
    upload_counter += 1

    file_name = str(ctx.author.id) + "-" + str(upload_counter)

    logging.info(f"{ctx.author} ({ctx.author.id}) has uploaded the file {file_name} to {attachment_cache_path}.")

    msg_attachment_url = ctx.message.attachments[0].url
    req = requests.get(msg_attachment_url)
    with open(attachment_cache_path + "/{}.png".format(file_name), "xb") as attachment:
        attachment.write(req.content)

    await ctx.send("File successfully saved as {}.".format(file_name))


bot.run(token)
