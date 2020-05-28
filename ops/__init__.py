from pathlib              import Path
from sys                  import stderr
from os.path              import dirname, basename
from ._utils              import filename
from itertools            import chain
from discord.ext.commands import (
    Cog, NoPrivateMessage,
    MissingPermissions,
    BotMissingPermissions
)
from importlib            import import_module

def _getall_cogs():
    # absoulte path to the module directory, where everything is stored in.
    __moddir_path__ = dirname(__file__)
    __moddir_name__ = basename(__moddir_path__)

    def _cogextract(module):
        # import the command module from the current directory.
        module = import_module(f'.{module}', __moddir_name__)

        cogs = getattr(module, '__cogexport__', None)
        return [] if not isinstance(cogs, list) else \
                filter(lambda cog: issubclass(cog, Cog), cogs)

    return chain(*map(lambda mod:
                _cogextract(filename.from_str(mod).name),
                    Path(__moddir_path__).glob('*.py')))

async def on_command_error(ctx, exc):
    """A custom `on_command_error` handler, handles some excpetions
    thrown in commands and translates into client compatible error
    messages for the command invoker/developer understand what had
    happened internally and possible reasons of this."""
    
    if isinstance(exc, NoPrivateMessage):
        await ctx.send("This command cannot be run outside the"
                       "context of a guild (eg. DMs, Group DMS).")
    elif isinstance(exc, (MissingPermissions, BotMissingPermissions)):
        await ctx.send(str(exc))  # send the message directly.
    else: stderr.write(str(exc))  # stderr: if can't be handled.

def setup(bot):
    for cog in _getall_cogs():
        bot.add_cog(cog())
    
    bot.event(on_command_error)