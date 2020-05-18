from   discord.ext.commands import Bot
from   os                   import getenv

bot = Bot('_', case_insensitive=True)

# all Cog registrations go here:
from cogs.basic import Basic
from cogs.games import Games

bot.add_cog(Basic())
bot.add_cog(Games())

# authorize by the token in the environment variables.
bot.run(getenv('DISCORD_ACCESS_TOKEN'))