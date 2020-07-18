# triabot
tripulse's own Discord bot which serves a lot of unique features that other bots fail to deliver.

---

## Programmers
As you may have probably guessed, this is written in Python 3 for doing the work with Discord it uses the
 sophisticated Discord.py API. You're assumed to have a little of experience with MongoDB.

### Installation
- clone the repository
- type in TTY `pip3 install -r requirements.txt`
- make a `config.yml` in the current folder, which defines how the bot acts, structure it somewhat like this:
  ```yaml
  credentials:
    discord:
      token: ''  # register your app then put the token.
    reddit:  # required for the 'meme' command.
      client_id: ''  # register an app on reddit then fill.
      client_secret: '' # ...
    mongodb_url: '' # setup a MongoDB database then retrieve the
                    # connection URI from the cluster.
  defaults:
    prefix: '.'  # set it to whatever you want.
  loglevel: 20  # means logging.INFO level.
  ```
   - Optionally, to configure the log-level in the console, set `loglevel` to any of [these values][1], by default it's
set to `INFO` level.

### Contribution
To contribute to this project you should follow the idioms described below, if not then core developers might have to
do extra effort cleaning up the code to match the idioms, sometimes not even accepting the PR.

#### Navigation
- `cogs` folder has all the command modules in it, each module is separated based on its usage.
    - `__init__.py` loads all command modules and handles their exceptions.
- `requirements.txt` is where all the required external dependencies stored in the `pip freeze` format.

#### Idioms
Moving to `cogs/` you'll see a lot of Python modules, each one has multiple categories referred to as so called "cogs
" in the Discord.py convention.

Categories are always that inherit from `Cog`. The syntax is somewhat like this:
```py
class MyCategory(Cog):
    ...
```

Free floating commands are not supported, they should be wrapped in a `Cog`. A command is a coroutine (aka. async
 function). Decorated with `command` and must accept a positional argument.
```py
class MyCategory(Cog):
    @command
    async def dosomething(ctx):
        ...
```

To export these classes to be picked up and be loaded, append a `__cogexport__` at the end all the class definitions
. It could be any iterable object that yields classes inherited from `Cog`, if not then the class is discarded.
```py
__cogexport__ = [MyCategory, SomeCategory]
```

The bot has a logger attached to it, which can be used later on for intentions of tracing back. In a command it can be
acquired through `ctx.bot.logger`.

[0]: https://api.mongodb.com/python/current/api/pymongo/database.html?highlight=database#pymongo.database.Database
[1]: https://docs.python.org/3.8/library/logging.html#logging-levels