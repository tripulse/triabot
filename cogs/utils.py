from discord.ext.commands import (
    check,
    NoPrivateMessage,
    MissingPermissions,
)

def author_has_guild_permissions(**perms):
    """Checks if the author of a message has guild permissions
    to perform a certain action."""
    def predicate(ctx):
        if not ctx.guild:
            raise NoPrivateMessage

        permissions = ctx.message.author.guild_permissions
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm, None) != value]

        if not missing:
            return True

        raise MissingPermissions(missing)

    return check(predicate)