from discord.ext.commands import Cog, command
from discord              import File, Embed

from .memegen.reddit import Reddit_partial
from random          import choice
from os              import getenv

class Memery(Cog):    
    """Sprinkle of internet humor from the major platforms to the obscure corners
    of the internet (eg. Reddit), might use some external APIs too"""

    _gens = {
        'reddit': Reddit_partial(getenv('RAPI_CLID'), getenv('RAPI_CLSECRET')),
    }

    @command()
    async def meme(self, ctx):
        """Cherrypicks a meme from anywhere it has reach to, this always posts an
        image as most of internet memes are made as images"""

        site = choice([*self._gens.keys()])
        pic, info = self._gens[site]()
        
        msg = Embed(title=info.get('title'), url=pic)
        msg.set_image(url=pic)
        msg.set_author(name=info.get('author'))

        await ctx.send(embed=msg)

__cogexport__ = [Memery,]