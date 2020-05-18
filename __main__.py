from   discord.ext.commands import Bot, check
from   discord              import Game, Status
from   os                   import getenv, listdir
from   checks               import is_bot_owner

bot = Bot('_', case_insensitive=True)

# Cogs loading
for cog in listdir("cogs"):
    if ".py" in cog:
        bot.load_extension("cogs." + cog.replace(".py", ""))

# Cogs reload command
@bot.command()
@check(is_bot_owner)
async def reload(ctx):
    await bot.change_presence(activity=Game("reloading ..."), status=Status.idle)
    message = await ctx.send("reloading...")
    for cog in listdir("cogs"):
        if ".py" in cog:
            if cog.replace(".py", "") in bot.cogs.keys():
                bot.reload_extension("cogs." + cog.replace(".py", ""))
            else:
                bot.load_extension("cogs." + cog.replace(".py", ""))
    await message.edit(content="reloaded!")
    await bot.change_presence(activity=None, status=Status.online)

# Stop command
@bot.command()
@check(is_bot_owner)
async def stop(ctx):
    await bot.logout()

# authorize by the token in the environment variables.
bot.run(getenv('DISCORD_ACCESS_TOKEN'))
