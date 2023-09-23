""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get
from settings import SPECIAL_ROLE, LOGS_CHANNEL
# Here we name the cog and create a new class for the cog.


class Moderator(commands.Cog, name="Moderator"):

  def __init__(self, bot):
    self.bot = bot

  # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
  @commands.hybrid_command(
      name="clear",
      description="Delete a number of messages.",
  )
  @commands.has_permissions(manage_messages=True)
  @commands.bot_has_permissions(manage_messages=True)
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
        description=
        f"**{ctx.author}** cleared **{len(purged_messages)-1}** messages!",
        color=0xBEBEFE,
    )
    await ctx.channel.send(embed=embed, delete_after=10)

  @commands.hybrid_command(
      name="nick",
      description="Change the nickname of a user on a server.",
  )
  @commands.bot_has_permissions(manage_nicknames=True)
  @app_commands.describe(
      user="The user that should have a new nickname.",
      nickname="The new nickname that should be set.",
  )
  async def nick(self,
                 ctx: Context,
                 user: discord.User,
                 *,
                 nickname: str = None) -> None:
    """
        Change the nickname of a user on a server.

        :param context: The hybrid command ctx.
        :param user: The user that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """

    member = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(
        user.id)
    special_role = get(ctx.message.guild.roles, id=int(SPECIAL_ROLE))

    if member.top_role.position > special_role.position:
      nickname = f"{nickname or member.display_name} {member.top_role.name.split(' ')[-1]}"

    await member.edit(nick=nickname)

  @nick.error
  async def missing_user(self, ctx: Context, error):
    if isinstance(error, commands.UserNotFound) or isinstance(
        error, commands.MissingRequiredArgument):
      member = ctx.author
      special_role = get(ctx.message.guild.roles, id=int(SPECIAL_ROLE))

      nickname = ctx.message.content.strip().removeprefix(
          'vnick').removeprefix('Vnick')
      await ctx.author.edit(nick=nickname)
      if member.top_role.position > special_role.position:
        await ctx.author.edit(nick=ctx.author.display_name + ' ' +
                              member.top_role.name.split(' ')[-1])

    else:
      await ctx.message.send(embed=discord.Embed(
          title=f"Error nick command!",
          description=str(error).capitalize(),
          color=0xE02B2B,
      ))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
  await bot.add_cog(Moderator(bot))
