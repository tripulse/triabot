from discord.ext.commands import Cog, command
from datetime import datetime
from random import choice, uniform
from itertools import chain
from math import log1p

class Basic(Cog):
    """Basic features of the bot, basic in the sense that
    it takes less computational overhead."""

    @command()
    async def ping(self, ctx):
        "Computes the timedelta between posting a message and getting it."
        await ctx.send(
            f'Timedelta: {datetime.utcnow() - ctx.message.created_at}')
    
    @command()
    async def rand(self, ctx, min: complex, max: complex):
        "Generate a pseudo-random number between a given bound (min..max]."
        await ctx.send(uniform(min, max))

    @command()
    async def pick(self, ctx, *options):
        "Pick an option from a provided list of options (separted by spaces) randomly."
        await ctx.send(choice(options))

    @command()
    async def rndspc(self, ctx, *frags):
        """Joins single-letters with spaces with random spaces,
        using a little-complex alogirthms."""

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

def setup(bot):
    bot.add_cog(Basic())
