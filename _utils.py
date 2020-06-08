from discord.ext.commands import HelpCommand
from discord              import Embed

class EmbedHelp(HelpCommand):
  """Help-command formatter that uses multiple embeds for each cogs or global level commands.
  It is considered better than the default formatter that multiple codeblocks as pages."""

  async def _prepare_command_desc(self, command) -> str:
    "Given a command prepare its description."

    # the signature is kept bold and the rest unchanged.
    return f"**{self.get_command_signature(command)}**\n{command.help}"

  async def send_bot_help(self, mappings):
    for cog, commands in mappings.items():
        await self._send_cog_help(cog, commands)
  
  async def send_cog_help(self, cog):
    await self._send_cog_help(cog, cog.get_commands())
  
  async def _send_cog_help(self, cog, commands):
    helpmsg = Embed(
      title=getattr(cog, 'qualified_name', None),
      description=getattr(cog, 'description', None))

    for command in await self.filter_commands(commands, sort=True):
      helpmsg.add_field(name=command.name, inline=False, value=
        self.prepare_help_command(command))
    
    await self.get_destination().send(embed=helpmsg)

  async def send_command_help(self, command):
    await self.get_destination().send(embed=
      Embed(title=command.name, description=self._prepare_command_desc(command)))

  async def send_group_help(self, group):
    helpmsg = Embed(title=group.name, description=self._prepare_command_desc(group))
      
    for command in group.commands:
      helpmsg.add_field(name=command.name, inline=False,
        value=self._prepare_command_desc(command))
      
    await self.get_destination().send(embed=helpmsg)
