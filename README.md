# waifu2x-discord-bot

A simple discord bot that runs a version of waifu2x to upscale an image a user has sent. 

NOTE: I used [waifu2x-ncnn-vulkan by nihui](https://github.com/nihui/waifu2x-ncnn-vulkan) as installation of waifu2x. If you wish to do otherwise, please note that while it *might* work as a drop-in solution, you may have to change some arguments in the subprocess.run() statement in main.py.

Feel free to open a (preferably descriptive) issue if you encounter any issues. Thanks.

How to use:

1. Setup variables in config.py:

  i. token = Your discord bot token. If you don't have one - follow [Discord.py's tutorial on how to make a bot account.](https://discordpy.readthedocs.io/en/latest/discord.html)
  
  ii. cache_path = An ***EMPTY*** folder for temporary storage of downloaded and upscaled images.
  
  iii. w2x_exec_path = A full path to your waifu2x executable.
  
  iv. cache_wipe_on_start = If set to True, it will delete *ALL* files in cache_path on startup. Highly reccomended - as False is not supported as of right now.
  
  v. logLevel = Valid values in decreasing levels of verbosity; DEBUG, INFO, WARN, ERROR, and CRITICAL. If you aren't sure - use INFO or WARN.
 
 2. Invite your bot. If you need help - see [Discord.py's tutorial on this.](https://discordpy.readthedocs.io/en/latest/discord.html#inviting-your-bot)
 
 3. Run main.py.
 
 4. Use 2x!upscale in a discord channel to upscale an image - like so.
 
 
 ![example](https://github.com/Sh211/waifu2x-discord-bot/blob/master/images/discordExample.png "An example of 2x!upscale")
