from os                   import getenv
from asyncio              import run
from discord.ext.commands import Bot

# initalise the bot instance with case sensitivity for
# command names and a static prefix of '.'
bot = Bot('.', case_insensitive=True)
bot.load_extension('ops')

try:
    bot.run(getenv('DAPI_ACCESS_TOKEN'))
except KeyboardInterrupt:
    run(bot.logout())
