from discord import Permissions
from discord.utils import escape_markdown
from discord.ext.commands import MissingPermissions

async def prefix(self, ctx, to_prefix: str = None):
    """Query the prefix of the current server of this bot, any text given is set the prefix."""

    current_prefix = (ctx.bot.db.read_guild_prefix(getattr(ctx.guild, 'id', None)) or
                      ctx.bot.config['defaults']['prefix'])

    if to_prefix:
        if not ctx.author.guild_permissions.manage_guild:
            raise MissingPermissions([Permissions.manage_guild])

            ctx.bot.db.write_guild_prefix(ctx.guild.id, to_prefix)
            await ctx.send(f'`{escape_markdown(current_prefix)}`' f' \u2192 '
                           f'`{escape_markdown(to_prefix)}`')
        else:

            await ctx.send(current_prefix)
