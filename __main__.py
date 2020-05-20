from os                   import getenv, listdir
from asyncio              import run
from sys                  import stderr

from discord.ext.commands import (
    Bot, check,
    NoPrivateMessage,
    MissingPermissions,
    BotMissingPermissions,
)

# some constants to work with, these are got from environ vars.
COMMODULES = getenv('COMMAND_MODULE_DIR', 'cogs')
MODEXCLUDES = ['utils.py']  # exclude some files from coglist.
BOTHOST_ID = getenv('BOT_HOST_ID')

bot = Bot('_', case_insensitive=True)

# Handles some exceptions if handler not defined print
# the traceback to the sys.stderr for debugging later on.
@bot.event
async def on_command_error(ctx, exc):
    if isinstance(exc, NoPrivateMessage):
        await ctx.send("This command cannot be run outside the"
                       "context of a guild (eg. DMs, Group DMS).")
    elif isinstance(exc, (MissingPermissions,
                          BotMissingPermissions)):
        await ctx.send(str(exc))
    else:  # if not handler satisfies the exception.
        stderr.write(str(exc))

@bot.command()
@check(lambda ctx: str(ctx.author.id) == BOTHOST_ID)
async def load(*_):
    for mod in listdir(COMMODULES):
        modname, _, ext = mod.partition('.')        
        if ext == 'py' and not mod in MODEXCLUDES:
            # choose whether to reload or just load based on
            # whether the module is already loaded or not.
            (bot.reload_extension if modname in bot.cogs.keys()
             else bot.load_extension)(f'{COMMODULES}.{modname}')

try:
    run(load())  # load all the command modules,
                 # at the startup.
    bot.run(getenv('DAPI_ACCESS_TOKEN'))
except KeyboardInterrupt:
    run(bot.logout())