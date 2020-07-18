from discord import Embed, Permissions
from discord.ext.commands import (
    Cog, Context, MissingPermissions,
    command
)

from utils.misc import get_color


class Core(Cog):
    """Controlling or using the core-functionalities of the bot."""

    @command()
    async def prefix(self, ctx: Context, to_prefix: str = None):
        """Query the prefix of the current server of this bot, any text given is set the prefix."""

        current_prefix = (ctx.bot.db.read_guild_prefix(ctx.guild.id) or
                          ctx.bot.config['defaults']['prefix'])

        if to_prefix:
            if not ctx.author.guild_permissions.manage_guild:
                raise MissingPermissions([Permissions.manage_guild])

            ctx.bot.db.write_guild_prefix(ctx.guild.id, to_prefix)
            await ctx.send(embed=Embed.from_dict({
                'title': f'Changed prefix',
                'fields': [{
                    'name': 'From',
                    'value': current_prefix,
                    'inline': True,
                }, {
                    'name': 'To',
                    'value': to_prefix,
                    'inline': True
                }],
                'color': get_color().value
            }))
        else:
            await ctx.send(embed=Embed.from_dict({
                'title': f'Current prefix',
                'description': current_prefix,
                'color': get_color().value
            }))


__cogexport__ = [Core]
