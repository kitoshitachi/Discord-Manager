""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
import os, platform, yaml

from logger import Logger
from settings import PREFIX_BOT
from discord.ext import commands
from discord.ext.commands import Context
from cores.helpcommand import CustomHelpCommand

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


class DiscordBot(commands.Bot):

	def __init__(self) -> None:
		super().__init__(
				command_prefix=PREFIX_BOT,
				intents=intents,
				help_command=CustomHelpCommand(),
		)
		self.logger = Logger
		with open('config.yml','r') as f:
			self.config = yaml.safe_load(f)
		self.logs_channel = self.get_partial_messageable(int(self.config['LOGS_CHANNEL']))

	async def load_cogs(self) -> None:
		"""
		Load all the cogs from the cogs folder.
		"""
		for file in os.listdir(
				f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
			if file.endswith(".py"):
				extension = file[:-3]
				try:
					await self.load_extension(f"cogs.{extension}")
					self.logger.info(f"Loaded extension '{extension}'")

				except Exception as e:
					exception = f"{type(e).__name__}: {e}"
					self.logger.error(f"Failed to load extension {extension}\n{exception}")


	async def setup_hook(self) -> None:
		'''
		This function is called when the bot is ready and logged in.
		'''
		self.logger.info(f"Logged in as {self.user.name}")
		self.logger.info(f"discord.py API version: {discord.__version__}")
		self.logger.info(f"Python version: {platform.python_version()}")
		self.logger.info(
				f"Running on: {platform.system()} {platform.release()} ({os.name})")
		self.logger.info("-------------------")

		await self.load_cogs()

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

