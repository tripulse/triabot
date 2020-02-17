"""A collection of basic commands that idol Discord bot should have."""
from discord.ext.commands import command, Context
from discord import Embed

from datetime import datetime
from numpy.fft import rfft
from functools import reduce
from random import choice


@command()
async def ping(ctx: Context):
    """Calculates the delta between message sent and message recieved.
    It's a mixture of multiple delays of arbitary time."""

    tdelta = datetime.utcnow() - ctx.message.created_at
    await ctx.send(f'\u0394`{tdelta}`')

@command()
async def computerfft(ctx: Context, *nums):
    """Computes 1D RFFT (real-valued fast-fourier transform) over arbitary
    numeric values separted with spaces."""
    
    invals = tuple(map(lambda n: float(n), nums))
    outvals = rfft(invals).tolist()

    await ctx.send(' '.join(map(
        lambda n: f'{str(n.real)}+i{str(n.imag)}',
    outvals)))

@command()
async def skwiggle(ctx: Context, *string_slices):
    """Idiotizes strings by randomizing the case of each letter.
    This method is mostly used to denote sentences/thoughts that are
    not in favour of the author."""

    instr = ' '.join(string_slices)
    await ctx.send(''.join([choice((c.upper, c.lower))() for c in instr]))

@command()
async def interjection(ctx: Context, thing: str= 'linux'):
    """Spits out a slice of the GNU/Linux interjection speech
    told by Richard M. Stallman at some point."""
    speech = f"I'd just like to interject for a moment. What you're referring to as {thing}, "\
             f"is in fact, GNU/{thing}, or as I've recently taken to calling it, GNU plus {thing}."

    await ctx.send(speech)


"""Collection of commands exported from this module."""
__commands__ = (ping, computerfft, skwiggle, interjection)
