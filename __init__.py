from   discord.ext.commands import *
from   os                   import getenv
from   itertools            import chain

import cogs.basic

bot = Bot('?', case_insensitive= True)

# all Cog registrations go here:
bot.add_cog(cogs.basic.Basic(bot))

# authorize by the token in the environment variables.
bot.run(getenv('DISCORD_ACCESS_TOKEN'))
