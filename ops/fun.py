from discord.ext.commands import Cog, command
from discord              import File, Embed

from .memegen.reddit import Reddit_partial
from random          import choice
from os              import getenv

class Memery(Cog):    
    """Sprinkle of internet humor from the major platforms
    to the obscure corners of the internet (eg. Reddit)."""
    _gens = {
        'reddit': Reddit_partial(
            getenv('RAPI_CLID'),
            getenv('RAPI_CLSECRET'))
    }

    @command()
    async def meme(self, ctx, site=''):
        """Cherrypick a meme from a site defined if cannot or
        not defined selects a random post from a random site."""

        if not site in self._gens:
            site = choice([*self._gens.keys()])

        pic, info = self._gens[site]()
        
        msg = Embed(title=info.get('title'))
        msg.set_image(url=pic)
        msg.set_author(name=info.get('author'))

        await ctx.send(embed=msg)
        

__cogexport__ = (Memery,)