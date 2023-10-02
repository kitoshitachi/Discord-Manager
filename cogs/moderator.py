""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import re
import discord
from discord import app_commands
from discord.ext.commands import (
  Context, Cog,
  hybrid_command, has_permissions, bot_has_permissions
)
from discord.utils import get
import yaml
# Here we name the cog and create a new class for the cog.


class Moderator(Cog, name="Moderator"):

  def __init__(self, bot):
    self.bot = bot
    with open('config.yml','r') as f:
      self.config = yaml.safe_load(f)

  # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
  @hybrid_command(
    name="clear",
    description="Delete a number of messages.",
  )
  @has_permissions(manage_messages=True)
  @bot_has_permissions(manage_messages=True)
  @app_commands.describe(
    amount="The amount of messages that should be deleted.")
  async def clear(self, ctx: Context, amount: int) -> None:
    """
      Delete a number of messages.

      :param context: The hybrid command ctx.
      :param amount: The number of messages that should be deleted.
      """
    await ctx.send("Deleting messages...")
    if amount > 99:
      amount = 99

    purged_messages = await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
      description=f"**{ctx.author}** cleared **{len(purged_messages)-1}** messages!",
      color=0xBEBEFE,
    )
    await ctx.channel.send(embed=embed, delete_after=10)

  @hybrid_command(
    name="nick",
    description="Change the nickname of a user on a server.",
  )
  @bot_has_permissions(manage_nicknames=True)
  @app_commands.describe(
    nickname="The new nickname that should be set.",
  )
  async def nick(self, ctx: Context, *, nickname: str = None) -> None:
    """
      Change the nickname of a user on a server.

      :param context: The hybrid command ctx.
      :param user: The user that should have its nickname changed.
      :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
      """
    nickname = re.sub('<@\d+>', '', ctx.message.content[5:]).strip()
    member = ctx.message.mentions[0] if ctx.message.mentions else ctx.author
    special_role = get(ctx.message.guild.roles, id=int(self.config['SPECIAL_ROLE']))
    if nickname is None or nickname == '':
      nickname = re.sub('[._ ]+', '', member.name)

    if member.top_role.position > special_role.position:
      nickname += '' + member.top_role.name.split(' ')[-1]

    await member.edit(nick=nickname)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.


async def setup(bot):
  await bot.add_cog(Moderator(bot))
