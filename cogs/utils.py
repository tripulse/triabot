from discord.ext.commands import (
    Cog,
    BucketType,
    command,
    has_permissions,
    bot_has_permissions,
    max_concurrency,
    group,
    has_guild_permissions,
    bot_has_guild_permissions,
)
from discord import (
    User,
    Embed,
    TextChannel,
)

from aioitertools import takewhile, map, filterfalse
from aioitertools.more_itertools import chunked
from utils.misc import get_member_color, aenumerate


class Utils(Cog):
    """Useful commands for making moderation easy on a guild."""

    @command()
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True, read_message_history=True)
    @max_concurrency(number=1, per=BucketType.channel)
    async def purge(self, ctx, num: int, *target: User):
        """Bulk delete messages of a certain amount posted by a targeted Discord user,
        if not provided a user it just deletes all the messages which it encounters"""

        total_deleted = 0
        messages = ctx.history(limit=None)
        await messages.__anext__()  # includes the invoker's message, so skip that.

        # discord has a bulk-deletion method which has limits that,
        # messages cannot be deleted older than 14 days.
        # cannot delete more than 100 messages at once.
        async for chunk in chunked(map(lambda m: m[1], takewhile(
                lambda m: m[0] < num and (ctx.message.created_at - m[1].created_at).days < 14,
                filterfalse(lambda m: not(m[1].author in target or not target), aenumerate(messages)))), 100):

            chunk = list(chunk)
            await ctx.channel.delete_messages(chunk)  # delete 100 messages at once.
            total_deleted += len(chunk)

        # for the rest follow the manual deletion way.
        async for msg in messages:
            if not total_deleted <= num:
                await ctx.send(f"Purged {num} messages in {ctx.channel.mention}.",
                               delete_after=8)
                break

            if msg.author == target or target is None:
                await msg.delete()
                total_deleted += 1

    @group(aliases=['movmsg'], invoke_without_command=True)
    @has_guild_permissions(manage_messages=True)
    @bot_has_guild_permissions(manage_messages=True)
    @max_concurrency(number=1)
    async def movemessage(self, ctx, channel: TextChannel, *message_ids: int):
        """Post some messages with certain IDs whose exist in the current channel to a destination channel.
        Message containing an embed is ignored."""

        for message_id in message_ids:
            msg_to_move = await ctx.channel.fetch_message(message_id)
            destination_msg = Embed.from_dict({
                'description': msg_to_move.content,
                'author': {
                    'name': msg_to_move.author.nick or msg_to_move.author.name,
                    'icon_url': str(msg_to_move.author.avatar_url)
                },
                'color': get_member_color(msg_to_move.author).value
            })

            if msg_to_move.attachments:
                destination_msg.add_field(name='Attachments',
                                          value='\n'.join(a.url for a in msg_to_move.attachments))

            destination_msg = await channel.send(embed=destination_msg)
            for reaction in msg_to_move.reactions:
                await destination_msg.add_reaction(reaction)

            await msg_to_move.delete()

    @movemessage.command(name='bulk')
    async def bulk_movemessage(self, ctx, dest: TextChannel, num: int):
        """Transfer atmost a given amount messages from the last sent message."""

        num = num + 1  # the message invoked this should stay intact.

        for msg in reversed(await ctx.history(limit=num).flatten()):
            if ctx.message.id != msg.id:
                await self.movemessage(ctx, dest, msg.id)


__cogexport__ = [Utils]