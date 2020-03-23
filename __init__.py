from   discord.ext.commands import *
from   os                   import getenv
from   itertools            import chain

import basic
import imgops

__commandcats__ = (basic,imgops) # list of command categories.

bot = Bot('?', case_insensitive= True)

for cmd in chain(*map(lambda cc: cc.__commands__, __commandcats__)):
    bot.add_command(cmd)

# authorize by the token in the environment variables.
bot.run(getenv('DISCORD_ACCESS_TOKEN'))
