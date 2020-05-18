from discord.ext.commands import Bot, check
from discord              import Status

import os
import re
import asyncio

bot = Bot('_', case_insensitive=True)

def is_bot_owner(ctx):
    """Check if a given message is posted by the hoster
    hosting it, configure environ: `HOST_DISCORD_ID`."""

    try:
        return ctx.author.id == int(os.getenv('HOST_DISCORD_ID'))
    except TypeError:
        return False

# a regular structure of a filename, including a name and a
# extension for hinting the user about the type of it.
filename = re.compile(r'^(?P<name>.*)\.(?P<ext>.*)$')

# reload function if required to reload all the Cogs.
@bot.command()
@check(is_bot_owner)
async def reload(*_):
    # load-in (if not already) or reload Cogs and move on.
    for mod in os.listdir('cogs'):
        modname, _, modext = mod.partition('.')
        if re.match('py', modext, re.I):            
            (bot.reload_extension if modname in bot.cogs.keys()
                else bot.load_extension)(f'cogs.{modname}')

# run the bot with a given token in DISCORD_ACCESS_TOKEN environ.
# if ctrl-c (^c) was pressed logout from API.
try:
    asyncio.run(reload())  # load all the modules at start.
    bot.run(os.getenv('DISCORD_ACCESS_TOKEN'))
except KeyboardInterrupt:
    asyncio.run(bot.logout())