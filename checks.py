from os import getenv

async def is_bot_owner(ctx):
    return ctx.author.id == int(getenv("OWNER_ID"))