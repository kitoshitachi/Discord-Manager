""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import os
import platform
import random
from logger import Logger
from datetime import datetime
from settings import DISCORD_TOKEN, LOGS_CHANNEL, SPECIAL_ROLE

import discord
from discord import Member
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import Context

from utils import embed_message

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


class DiscordBot(commands.Bot):

  def __init__(self) -> None:
    super().__init__(
        command_prefix=commands.when_mentioned_or('v', 'V'),
        intents=intents,
        help_command=None,
    )
    self.logger = Logger
    self.logs_channel = self.get_partial_messageable(int(LOGS_CHANNEL))

  async def load_cogs(self) -> None:
    for file in os.listdir(
        f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
      if file.endswith(".py"):
        extension = file[:-3]
        try:
          await self.load_extension(f"cogs.{extension}")
          self.logger.info(f"Loaded extension '{extension}'")

        except Exception as e:
          exception = f"{type(e).__name__}: {e}"
          self.logger.error(
              f"Failed to load extension {extension}\n{exception}")
          embed = discord.Embed(
              title=f"Error load cogs",
              description=f"Failed to load extension {extension}\n{exception}",
              timestamp=datetime.now(),
              color=discord.Color.red())

          await self.logs_channel.send(embed=embed)

  @tasks.loop(minutes=5.0)
  async def status_task(self) -> None:
    """
        Setup the game status task of the bot.
        """
    Activities = [
        discord.CustomActivity(name="Drinking !", emoji='🍷'),
        discord.CustomActivity(name="Fighting !", emoji='⚔️'),
        discord.CustomActivity(name="Sleeping !", emoji='⚰️'),
    ]
    await self.change_presence(status=discord.Status.online,
                               activity=random.choice(Activities))

  @status_task.before_loop
  async def before_status_task(self) -> None:
    await self.wait_until_ready()

  async def setup_hook(self) -> None:
    self.logger.info(f"Logged in as {self.user.name}")
    self.logger.info(f"discord.py API version: {discord.__version__}")
    self.logger.info(f"Python version: {platform.python_version()}")
    self.logger.info(
        f"Running on: {platform.system()} {platform.release()} ({os.name})")
    self.logger.info("-------------------")

    await self.load_cogs()
    self.status_task.start()

  async def on_message(self, message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    if message.author == self.user or message.author.bot:
      return
    await self.process_commands(message)

  async def on_command_completion(self, context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed.

    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if executed_command != 'clear':
      await context.message.add_reaction('✅')
    content = f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
    self.logger.info(content)
    

  async def on_command_error(self, context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error.

    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """

    if isinstance(error, commands.CommandOnCooldown):
      minutes, seconds = divmod(error.retry_after, 60)
      hours, minutes = divmod(minutes, 60)
      hours = hours % 24
      embed = discord.Embed(
          description=
          f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
          color=0xE02B2B,
      )
      await context.channel.send(embed=embed, delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(
          description="You are missing the permission(s) `" +
          ", ".join(error.missing_permissions) + "` to execute this command!",
          color=0xE02B2B,
      )
      await context.channel.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):

      embed = discord.Embed(
          description="I am missing the permission(s) `" +
          ", ".join(error.missing_permissions) +
          "` to fully perform this command!",
          color=0xE02B2B,
      )
      await context.channel.send(embed=embed)

  async def on_member_update(self, before: Member, after: Member) -> None:
    special_role = get(after.guild.roles, id=int(SPECIAL_ROLE))

    if before.top_role.name != after.top_role.name:
      display_name = after.display_name  #or after.name
      if after.top_role.position > special_role.position:
        if before.top_role.position > special_role.position:
          display_name = display_name.split(' ')
          display_name.pop()
          display_name = ' '.join(display_name)

        display_name = f"{display_name} {after.top_role.name.split(' ')[-1]}"

      elif after.top_role.position < special_role.position and before.top_role.position > special_role.position:
        display_name = display_name.split(' ')
        display_name.pop()
        display_name = ' '.join(display_name)

      await after.edit(nick=display_name)


# keep_alive()

bot = DiscordBot()
bot.run(DISCORD_TOKEN)
