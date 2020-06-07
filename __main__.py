from os                   import getenv
from asyncio              import run
from discord.ext.commands import Bot

# initalise the bot instance with case sensitivity for
# command names and a static prefix of '.'
bot = Bot('.', case_insensitive=True)
bot.load_extension('ops')

# override the code-block version of help-formatter
from _utils import EmbedHelp
bot.help_command = EmbedHelp()

try:
    bot.run(getenv('DAPI_ACCESS_TOKEN'))
except KeyboardInterrupt:
    run(bot.logout())
