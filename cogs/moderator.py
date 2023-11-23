#standard library imports
import re
from typing import Optional

# Third-party imports
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import (
  Context, Cog,
  has_permissions, bot_has_permissions
)
from discord.utils import get
import yaml
# Here we name the cog and create a new class for the cog.


class Moderator(Cog, name="Moderator"):

    def __init__(self, bot):
        self.bot = bot
        with open('config.yml', 'r') as f:
            self.config = yaml.safe_load(f)

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(name="clear",
                    description="Delete a number of messages.",
                    aliases=['purge', 'delete'])
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    @commands.app_commands.describe(
        amount="The amount of messages that should be deleted.")
    async def clear(self, ctx: Context, amount: int) -> None:
        """
      Delete a number of messages.

      :param context: The hybrid command ctx.
      :param amount: The number of messages that should be deleted.
      """
        await ctx.send("Deleting messages...")
        amount += 1
        if amount > 99:
            amount = 99

        messages = await ctx.channel.history(limit=amount).flatten()
        await ctx.channel.delete_messages(messages)
        embed = discord.Embed(
            description=
            f"**{ctx.author}** cleared **{len(messages)-1}** messages!",
            color=0xBEBEFE,
        )
        await ctx.channel.send(embed=embed, delete_after=10)

    @commands.hybrid_command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @bot_has_permissions(manage_nicknames=True)
    @commands.app_commands.describe(nickname="The new nickname that should be set.", )
    async def nick(self,
                   ctx,
                   user: Optional[Member] = None,
                   *,
                   nickname: Optional[str] = None):
        """
    :param context: The hybrid command ctx.
    :param user: The user that should have its nickname changed.
    :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
    """
        member = user or ctx.author
        special_role = get(ctx.guild.roles,
                           id=int(self.config['SPECIAL_ROLE']))

        if nickname:
            nickname = re.sub('<@\d+>', '', nickname).strip()

        if not nickname:
            nickname = re.sub('[._ ]+', '', member.name)

        if member.top_role.position > special_role.position:
            nickname += ' ' + member.top_role.name.split(' ')[-1]

        await member.edit(nick=nickname)

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member) -> None:
        special_role = get(after.guild.roles,
                           id=int(self.config['SPECIAL_ROLE']))

        if before.top_role.name != after.top_role.name:
            display_name = after.display_name  # or after.name
            top_role_name_last_part = after.top_role.name.rsplit(' ', 1)[-1]

            if after.top_role.position > special_role.position:
                if before.top_role.position > special_role.position:
                    display_name = display_name.rsplit(' ', 1)[0]

                display_name = f"{display_name} {top_role_name_last_part}"

            elif after.top_role.position < special_role.position and before.top_role.position > special_role.position:
                display_name = display_name.rsplit(' ', 1)[0]

            await after.edit(nick=display_name)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.


async def setup(bot):
    await bot.add_cog(Moderator(bot))
