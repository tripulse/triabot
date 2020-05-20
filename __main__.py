from discord.ext.commands import Bot, check
from os                   import getenv, listdir
from os.path              import join, sep
from asyncio              import run

# some constants to work with, these are got from environ vars.
COMMODULES = getenv('COMMAND_MODULE_DIR', 'cogs')
BOTHOST_ID = getenv('BOT_HOST_ID')

bot = Bot('_', case_insensitive=True)

@bot.command()
@check(lambda ctx: str(ctx.author.id) == BOTHOST_ID)
async def load(*_):
    for mod in listdir(COMMODULES):
        modname, _, ext = mod.partition('.')        
        if ext == 'py':
            # choose whether to reload or just load based on
            # whether the module is already loaded or not.
            (bot.reload_extension if modname in bot.cogs.keys()
             else bot.load_extension)(f'{COMMODULES}.{modname}')

try:
    run(load())  # load all the command modules,
                 # at the startup.
    bot.run(getenv('DISCORD_ACCESS_TOKEN'))
except KeyboardInterrupt:
    run(bot.logout())