"""A collection of basic commands that idol Discord bot should have."""
from discord.ext.commands import Command, Context
from discord import Embed

from datetime import datetime
from numpy.fft import rfft
from functools import reduce
from random import choice

class BasicCommand(Command):
    def __init__(self):
        Command.__init__(self, name= type(self).__name__, 
                               func= self._run, 
                               help= self.__doc__)

class ping(BasicCommand):
    """Calculates the delta between message sent and message recieved.
    It's a mixture of multiple delays of arbitary time."""

    @classmethod
    async def _run(cls, ctx: Context):
        tdelta = datetime.utcnow() - ctx.message.created_at
        await ctx.send(f'\u0394`{tdelta}`')

class computerfft(BasicCommand):
    """Computes 1D RFFT (real-valued fast-fourier transform) over arbitary
    numeric values separted with spaces."""

    @classmethod
    async def _run(cls, ctx: Context, *nums):
        invals = tuple(map(lambda n: float(n), nums))
        outvals = rfft(invals).tolist()

        await ctx.send(' '.join(map(
            lambda n: f'{str(n.real)}+i{str(n.imag)}',
        outvals)))

class skwiggle(BasicCommand):
    """Idiotizes strings by randomizing the case of each letter.
    This method is mostly used to denote sentences/thoughts that are
    not in favour of the author."""

    @classmethod
    async def _run(cls, ctx: Context, *string_slices):
        instr = ' '.join(string_slices)
        await ctx.send(''.join([choice((c.upper, c.lower))() for c in instr]))

"""List of commands available in this single module."""
__commands__ = (ping, computerfft, skwiggle)
