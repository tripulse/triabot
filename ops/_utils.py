from urllib.parse         import urlparse
from os.path              import basename
from sys                  import stderr
from typing               import NamedTuple, Union
from discord.ext.commands import (
    check,
    NoPrivateMessage,
    BotMissingPermissions,
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

class filename(NamedTuple):
    """Reprents a structure of a general filename structre which has a
    extension identifier sticked to it for covinience. this does all
    structuring (`from_*`) and de-structuring (`__str__`)."""

    name: str
    ext:  str

    @staticmethod
    def from_str(path: str):
        """Build from a string which is a filename. If given string was
        a path it extracts the filename out of it.
        
        NOTE: this doesn't check for a filename being compilant to an OS."""
        
        path = str(path)  # force convert to a string.
        name, _, ext = basename(path).rpartition('.')
        
        return filename(name, ext)

    @staticmethod
    def from_url(url: str):
        """Same as `filename.from_str()` but constructs from a URL."""
        return filename.from_str(urlparse(url)[2])

    def __str__(self):
        return f'{self.name}.{self.ext}'