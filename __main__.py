from   discord.ext.commands import Bot, check
from   discord              import Game, Status
from   os                   import getenv, listdir
from   checks               import is_bot_owner

bot = Bot('_', case_insensitive=True)

# Cogs loading
for cog in listdir("cogs"):
    if ".py" == cog[-3:]:
        bot.load_extension("cogs."+cog[:-3])

# Cogs reload command
@bot.command()
@check(is_bot_owner)
async def reload(ctx):

    await bot.change_presence(status=Status.idle)

    for cog in listdir("cogs"):
        if ".py" == cog[-3:]:
            if cog[:-3] in bot.cogs.keys():
                bot.reload_extension("cogs."+cog[:-3])
            else:
                bot.load_extension("cogs."+cog[:-3])
    
    await bot.change_presence(status=Status.online)

# Stop command
@bot.command()
@check(is_bot_owner)
async def stop(ctx):
    await bot.logout()

# authorize by the token in the environment variables.
bot.run(getenv('DISCORD_ACCESS_TOKEN'))