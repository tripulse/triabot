"""
These commands serve as operational commands for manipulating
image data without doing any sort of filtering on pixels except
when encoding to different format (eg. WebP).
"""

from discord.ext.commands import command, Context
from discord              import File
import requests
from io                   import BytesIO

@command()
async def pngminify(ctx: Context, url: str= None):
    """
    pngminify uses the 'pngmin' API which strips out ancillary
    information from PNG files and reduces file size slightly,
    useful when stripping out tracking information (eg. EXIF).
    """
    for attachment in ctx.message.attachments:
        if attachment.size < 57:
            await ctx.send("Invalid PNG file size as of specification.")

        attachment = await attachment.to_file()
        png_sig = attachment.fp.read(8)
        if b'\x89PNG\r\n\x1a\n' != png_sig:
            await ctx.send("Invalid PNG signature found in the beginning.")

        outimg = requests.post('https://pngmin.herokuapp.com/', png_sig + attachment.fp.read())

        if outimg.status_code == 415:
            await ctx.send("Failed to parse the PNG file correctly.")

        await ctx.send(file= File(BytesIO(outimg.content), filename= attachment.filename))

__commands__ = (pngminify,)