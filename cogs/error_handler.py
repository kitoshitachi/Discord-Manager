""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context, Cog
from cores.database import Database
from discord.ext.commands import CommandOnCooldown, MissingPermissions, BotMissingPermissions, CommandNotFound

class ErrorHandler(commands.Cog, name="error_handler"):
	def __init__(self, bot):
		self.bot = bot
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
			hours = hours % 24
			await context.channel.send(content=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
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
			print(error)
			await context.channel.send(content=str(error).capitalize())
		

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
	await bot.add_cog(ErrorHandler(bot))