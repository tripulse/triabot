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
    async def ping(self, ctx):
        "Computes the timedelta between posting a message and getting it."
        await ctx.send(
            f'Timedelta: {datetime.utcnow() - ctx.message.created_at}')
    
    @command()
    async def rand(self, ctx, min: float, max: float):
        "Generate a pseudo-random number between a given bound (min..max]."
        await ctx.send(uniform(min, max))

    @command()
    async def pick(self, ctx, *options):
        "Pick an option from a provided list of options (separted by spaces) randomly."
        await ctx.send(choice(options))

    @command()
    async def rndspc(self, ctx, *frags):
        """Joins single-letters with spaces with random spaces, using a little-complex alogirthms."""

        await ctx.send(''.join(
            c + ' ' * int(log1p(i)) for i,c in
                enumerate(chain(*frags))))

    @command()
    async def rndcap(self, ctx, *frags):
        """Does alternate capitalization of text, this is mostly
        used to say a wrong statement in sarcastic way. See this:
        https://english.stackexchange.com/q/533036"""

        await ctx.send(''.join(
            choice([c.upper, c.lower])() for c in
                ' '.join(frags)))

class Utils(Cog):
    """Contains utilities for Discord moderation, though these features
    are not all unique but just for covinience. Tools include such as —
    message purging, etc."""

    @command()
    @author_has_guild_permissions(manage_messages=True)
    @bot_has_guild_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, target: User, num: int=10):
        """Bulk delete messages of a certain amount posted
        by a targetted Discord user."""

        msgs_deleted = 0
        async for msg in ctx.history(limit=None):
            if not msgs_deleted < num: break
            if msg.author == target:
                await msg.delete()
                msgs_deleted+= 1

        await ctx.send(f"Purged {msgs_deleted} messages sent by @{target.tag}.")

__cogexport__ = [Basic, Utils]