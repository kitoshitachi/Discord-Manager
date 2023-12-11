


#Third Party Library
from datetime import time
import discord
from discord.ext import commands
from discord.ext.commands import Context, Cog
from discord.ext.commands import (
	CommandOnCooldown, 
	MissingPermissions, BotMissingPermissions, 
	CommandNotFound
)
from cores.utils import remaining_time
#Local Application/Library Specific
from logger import Logger
from settings import CONFIG
from cores.database import Database

class Handler(commands.Cog, name="handler"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.config = CONFIG
		self.logger = Logger
		self.supabase = Database()

	@Cog.listener()
	async def on_command_error(self, context: Context, error) -> None:
		"""
		The code in this event is executed every time a normal valid command catches an error.

		:param context: The context of the normal command that failed executing.
		:param error: The error that has been faced.

		"""
		if isinstance(error, CommandNotFound):
			return

		if isinstance(error, CommandOnCooldown):
			minutes, seconds = divmod(error.retry_after, 60)
			hours, minutes = divmod(minutes, 60)
			days, hours = divmod(hours, 24)
			print(days, hours)
			await context.channel.send(
				content=f"**Please slow down** - You can use this command again in {remaining_time(days, hours, minutes, seconds)}.",
				delete_after=10)
			
		elif isinstance(error, MissingPermissions):
			embed = discord.Embed(
				description="You are missing the permission(s) `" +
				", ".join(error.missing_permissions) + "` to execute this command!",
				color=0xE02B2B,
			)
			await context.channel.send(embed=embed)
		elif isinstance(error, BotMissingPermissions):
			embed = discord.Embed(
				description="I am missing the permission(s) `" +
				", ".join(error.missing_permissions) +
				"` to fully perform this command!",
				color=0xE02B2B,
			)
			await context.channel.send(embed=embed)
		else:
			await context.channel.send(content=str(error).capitalize())
			self.logger.error(error)
		
		await context.message.add_reaction(self.config['ERROR_EMOJI'])
	
	
	@Cog.listener()
	async def on_command_completion(self, context: Context) -> None:
		"""
		The code in this event is executed every time a normal command has been *successfully* executed.

		:param context: The context of the command that has been executed.
		"""
		full_command_name = context.command.qualified_name
		split = full_command_name.split(" ")
		executed_command = str(split[0])
		if executed_command != 'clear':
			await context.message.add_reaction(self.config['SUCCESS_EMOJI'])
		content = f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
		self.logger.info(content)





# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Handler(bot))