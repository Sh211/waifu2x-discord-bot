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
    print("Logged in as {}!".format(bot.user))
    logging.info("Logged in as {}, ID {}.".format(bot.user, bot.user.id))


@bot.command()
async def ping(ctx):
    print(ctx.author.id)
    await ctx.send("Pong! You are user {}, or id {}.".format(ctx.author, ctx.author.id))


@bot.command()
async def upload(ctx):
    global upload_counter
    upload_counter += 1

    cmd_author = ctx.author.id
    file_name = str(cmd_author) + "-" + str(upload_counter)

    msg_attachment_url = ctx.message.attachments[0].url
    req = requests.get(msg_attachment_url)
    with open(attachment_cache_path + "/{}.png".format(file_name), "xb") as attachment:
        attachment.write(req.content)

    await ctx.send("File successfully saved as {}.".format(file_name))


bot.run(token)
