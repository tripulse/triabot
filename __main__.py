import re
import logging
import yaml

from discord.ext.commands import Bot
from utils.database import BotDatabase
from utils.help_command import DecoratedHelpCommand
from pymongo.errors import (
    InvalidURI,
    ConnectionFailure,
    ConfigurationError
)

from typing import List
from utils.misc import subscript
from schema import (
    Schema, SchemaError, And, Optional
)


class Triabot(Bot):
    # schematic to detect proper configuration files, them being wrong causes a fatal error.
    CONFIG_SCHEMA = Schema({
        'credentials': {
            'discord': {'token': str},
            'reddit': {
                'client_id': str,
                'client_secret': str
            },
            'mongodb_url': str
        },
        'defaults': {
            'prefix': And(str, lambda p: 0 < len(p) <= 2000)
        },
        Optional('loglevel', default=logging.INFO): int
    })

    @classmethod
    def extract_prefix(cls, bot, message) -> List[str]:
        """Get bot prefix based on the guild configurations, also if the bot user was explicitly mentioned then
        regardless of the guild prefix it responds to the invoker.

        :param message: the message that the bot received.
        :returns: a list of prefixes to match on.
        """

        # get the guild specific prefix or else default to the specified one defined
        # inside a environment variable (it must be defined there).
        prefixes = [bot.db.read_guild_prefix(getattr(message.guild, 'id', None)) or bot.config['defaults']['prefix']]

        # if there was mention as a prefix then listen to that.
        if _prefix := subscript(re.match(rf'^(<@!{bot.user.id}>\s*)', message.content), 0):
            prefixes.append(_prefix)

        return prefixes

    async def on_ready(self):
        self.logger.info("Bot has been started!")

    def __init__(self, config_file):
        try:
            config = self.CONFIG_SCHEMA.validate(yaml.load(config_file))
        except SchemaError as schmerr:
            logging.exception("Invalid configuration schema", exc_info=schmerr)
            exit()
        except yaml.YAMLError as fmterr:
            logging.exception("Invalid YAML file", exc_info=fmterr)
            exit()

        self.logger = logging.getLogger('discord')
        self.logger.setLevel(config['loglevel'])

        try:
            database = BotDatabase(config['credentials']['mongodb_url'])
        except (InvalidURI,
                ConnectionFailure,
                ConfigurationError) as dberr:
            logging.exception("MongoDB database initialization failed", exc_info=dberr)
            exit()

        self.db, self.config = database, config
        super().__init__(self.extract_prefix, DecoratedHelpCommand())

    def run(self):
        super().run(self.config['credentials']['discord']['token'])


if __name__ == '__main__':
    from utils import core_commands

    # the bot instance, that'll drive the entire thing.
    bot = Triabot(open('config.yml'))

    bot.load_extension('cogs')
    bot.command(core_commands.prefix)

    from keep_alive import app
    from threading import Thread

    # host the Flask server on the separate thread, to prevent blocking.
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8000}).start()

    bot.run()

