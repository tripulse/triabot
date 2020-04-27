from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime
from random import choice

class Basic(Cog):
    """Basic features of the bot, basic in the sense that
    it takes less computational overhead."""

    @command()
    async def ping(self, ctx):
        "Computes the timedelta between posting a message and getting it."
        await ctx.send(
            f'Timedelta: {datetime.utcnow() - ctx.message.created_at}')

    @command()
    async def pick(self, ctx, *options):
        "Pick an option from a provided list of options (separted by spaces) randomly."
        await ctx.send(choice(options))