
# STANDARD MODULES
import os, platform
from typing import Any, Callable, Optional

# THIRD PARTY MODULES
import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command

# LOCAL MODULES
from logger import Logger
from settings import CONFIG, PREFIX_BOT
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
		self.config = CONFIG

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

	def get_command(self, name: str) -> Command[None, Callable[..., Any], Any] | None:
		
		return super().get_command(name.lower())
	
	def get_cog(self, name: str) -> Cog | None:
		name = name.lower()
		
		return super().get_cog(name)

	