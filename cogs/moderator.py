#standard library imports
import re
from typing import Optional

# Third-party imports
from discord import Member, utils
from discord.ext import commands
from discord.ext.commands import (
  Context, Cog,  # Context and Cog are required for the bot to work.
  has_permissions, bot_has_permissions,  # Check if the bot has the required permissions.
)

# Local application/library specific imports
import cores.parameters as parameter
from settings import CONFIG

_extract_username = re.compile(r"[._ ]+").sub # regex to extract username

class Moderator(Cog, name="moderator"):
    """
    **🕵️ Moderator**
    It contains all the moderation commands.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = CONFIG

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(name="clear",
                    description="Delete a number of messages.",
                    aliases=['purge', 'delete'])
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(self, ctx: Context, limit: int = parameter.limit) -> None:
        """
        Delete a number of messages.

        :param context: The hybrid command ctx.
        :param amount: The number of messages that should be deleted.
        """
        await ctx.send("Deleting messages...")
        limit += 1
        if limit > 99:
            limit = 99

        messages = await ctx.channel.purge(limit=limit)
        await ctx.send(content=f"**{ctx.author}** cleared **{len(messages)}** messages!", 
                       delete_after=10)

    @commands.hybrid_command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @bot_has_permissions(manage_nicknames=True)
    async def nick(self, ctx: Context, member: Optional[Member] = parameter.member, *, nickname: Optional[str] = parameter.nickname):
        """
        Change the nickname of a user on a server.
        
        Parameters
        -----------
        member: :class:`discord.Member` or `~discord.User` or :class:`str`
            The member or user that was requested.
        nickname: :class:`str`
            The new nickname.
        """
        
        

        special_role = utils.get(ctx.guild.roles, id=int(self.config['SPECIAL_ROLE']))
        
        if member.top_role.position > special_role.position:
            nickname += ' ' + member.top_role.name.split(' ')[-1]

        nickname = nickname.strip().capitalize()

        await member.edit(nick=nickname)

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member) -> None:
        special_role = utils.get(after.guild.roles, id=int(self.config['SPECIAL_ROLE']))

        if before.top_role.name != after.top_role.name:
            display_name = after.display_name

            if after.top_role.position > special_role.position:
                display_name_parts = [display_name]
                top_role_name_parts = after.top_role.name.split(' ')
                if len(top_role_name_parts) > 1:
                    display_name_parts.append(top_role_name_parts[-1])
                display_name = ' '.join(display_name_parts)

            elif after.top_role.position < special_role.position and before.top_role.position > special_role.position:
                display_name_parts = display_name.split(' ')
                if len(display_name_parts) > 1:
                    display_name = ' '.join(display_name_parts[:-1])

            await after.edit(nick=display_name)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderator(bot))
