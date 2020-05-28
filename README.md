<h1 align=center>triabot</h1>
<p align=center>tripulse's own Discord bot which serves a lot of unique features that other bots fail to deliver. This is mostly used for general purpose stuff (eg. slight moderation, text/media manipulation).</p>

> The internal structures are now stabilized so as the features are. Updates will be pushed at random intervals but gurantee stability, if still a bug is found report to "Issues" tab.

---

## Programmers
As you may have probably guessed, this is written in Python 3 and uses the newest syntax from Python 3.8, for doing the I/O with Discord it uses the good 'ol discord.py.

### Installation
- clone the repository
- type in TTY `pip3 install -r requirements.txt`
- get a bot token from Discord API
  - put token in `DAPI_ACCESS_TOKEN` environ
- get Client ID, Client Secret from Reddit API
  - put Client ID in `RAPI_CLID` environ
  - put Client Secret in `RAPI_CLSECRET` environ


### Contribution
To contribute you must follow some of the idioms of coding in this bot. We spent a lot of time cleaning out the module dependency structure for the sake of cleaniness.

#### Navigation
- `ops` folder has all the command modules in it. Subfolders inside it work as modules for the commands to reuse, those have no gurantee of being documented.
    - `__init__.py` is where all the command modules are managed, it mostly consists of event listeners, module loaders and text-formatters as of now.
- `requirements.txt` is where global dependencies should
be stored, if a command module requires a certain dependency one specify which dependency what version of it, it's is discouraged use broken or unstable dependencies.

#### Idioms
Moving to `ops/` you see a lot of Python modules, each one has multiple categories referred to as so called "cogs" in the discord.py convention.

Categories are always classes that inherit from `Cog`. The syntax is somewhat like this:
```py
class MyCategory(Cog):
    ...
```

Commands are encapsulated/contained in these categories as methods of the class. Each command should be a coroutine object (in simple terms: an `async` function definition). Which is decorated always decorated with `command` and accept atleast one positional arugment.

```py
class SomeCategory(Cog):
    @command
    async def dosomething(ctx):
        ...
```

To export all the definitions of each category append a `__cogexport__` at the end of all definitions to be exported, this is a `list` type (if not then just does nothing). If this was not a subclass of `Cog` this will just be discarded.

```py
__cogexport__ = [MyCategory, SomeCategory]
```