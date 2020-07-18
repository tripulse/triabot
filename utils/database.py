from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from typing import Optional
from utils.misc import subscript


class BotDatabase:
    """An abstraction over the MongoDB API for doing several operations that require a non-volatile storage.

    Currently it's capable of doing these operations:

    - Guild specific prefix (getting/setting).
    """

    def __init__(self, db_uri):
        """
        :param db_uri: MongoDB URI to connect to, it connects to a MongoDB cluster,
                       it must contain a DB name in the URI.

        :raises InvalidURI: if MongoDB URI was malformed.
        :raises ConnectionFailure: if cannot connect to a cluster.
        :raises ConfigurationError: if no database name was already given.
        """

        self._database = MongoClient(db_uri).get_default_database()

        # create the collection if they don't exist already.
        try:
            self._collections = {
                'prefixes': self._database.create_collection('prefixes'),
            }
        except CollectionInvalid:
            self._collections = {
                'prefixes': self._database.get_collection('prefixes'),
            }

    def write_guild_prefix(self, guild_id: int, prefix: str):
        """Add/update a guild-specific prefix in the registry, tied to a guild ID.

        :param guild_id: the Snowflake of a guild.
        :param prefix: prefix for the bot respond to.
        """

        self._collections['prefixes'].update_one({'guild_id': guild_id},
                                                 {'$set': {'prefix': prefix}},
                                                 upsert=True)

    def read_guild_prefix(self, guild_id: int) -> Optional[str]:
        """Get the guild-specific prefix for guild by its ID.

        :param guild_id: the Snowflake of a guild.
        :return: prefix for the guild (can be nothing).
        """

        return subscript(self._collections['prefixes'].find_one({'guild_id': guild_id}),
                         'prefix')
