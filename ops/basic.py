from discord              import User
from discord.ext.commands import (
    Cog, command,
    bot_has_guild_permissions
)

from datetime             import datetime, timedelta
from random               import choice, uniform
from itertools            import chain
from math                 import log1p
from ._utils              import (
    author_has_guild_permissions
)

class Basic(Cog):
    @command()
    async def test(self, ctx):
        """This command is verify that the bot's command parsing algorithm is working
        fine, it returns the WebSocket delay in miliseconds"""

        await ctx.send(f"{round(ctx.bot.latency * 1000, 2)}ms")

    @command()
    async def rand(self, ctx, min: float, max: float):
        """Given a decimal bound as (min..max] it uses uniform distribution to pick
        a pseudo-random number from that range"""

        await ctx.send(uniform(min, max))

    @command()
    async def rndpick(self, ctx, *options):
        """Given a arbitrary number of options to choose from, this chooses an option
        from list of those pseudo-randomly"""

        await ctx.send(choice(options))

    @command()
    async def space(self, ctx, spaces: int, *, text: str):
        """Spaces characters with a defined amount to E M P H A S I Z E a statement, these
        are mostly used to exaggerate some statement (eg. A  E  S  T  H  E  T  I  C  S)"""

        await ctx.send(''.join(c + ' ' * spaces for c in text))

    @command()
    async def rndcap(self, ctx, *, text: str):
        """Randomly capitalizes each and every English word of a text to emphasize the
        text as if it was wrong in a ironic way. For information:
        https://english.stackexchange.com/q/533036"""

        await ctx.send(''.join(choice([c.upper, c.lower])() for c in text))

class Utils(Cog):
    """Contains utilities for Discord moderation, though these features
    are not all unique but just for covinience. Tools include such as —
    message purging, etc."""

    @command()
    @author_has_guild_permissions(manage_messages=True)
    @bot_has_guild_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, num: int=10, target: User=None):
        """Bulk delete messages of a certain amount posted by a targetted Discord user,
        if not provided a user it just deletes all the messages which it encounters"""

        msgs_deleted = 0
        async for msg in ctx.history(limit=None):
            if not msgs_deleted < num:
                await ctx.send(f"Purged {num} messages in {ctx.channel}.")
                break
            if msg.author == target or target is None:
                await msg.delete()
                msgs_deleted+= 1
        
__cogexport__ = [Basic, Utils]