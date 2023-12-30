#standard library imports

# Third-party imports
from typing import Optional
from discord import Member, utils
from discord.ext import commands
from discord.ext.commands import (
  Context, Cog, 
  has_permissions, bot_has_permissions
)

# Local application/library specific imports
import parameter
from core import clean_name, deEmojify
from settings import CONFIG

class Moderator(Cog, name="moderator"):
	"""
	**🕵️ Moderator**
	It contains all the moderation commands.
	"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.config = CONFIG
		self.special_role = None

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
	async def nick(self, ctx: Context, member: Optional[Member], *, nickname:Optional[str] = parameter.nickname):
		"""
		Change the nickname of a user on a server.
		
		Parameters
		-----------
		member: :class:`discord.Member` or `~discord.User` or :class:`str`
			The member or user that was requested.
		nickname: :class:`str`
			The new nickname.
		"""
		try:
			if member == None:
				member = ctx.message.mentions.pop(0)
		except IndexError:
			member = ctx.author

		if nickname == None:
			nickname = member.global_name or clean_name(member.name)
		
		special_role = utils.get(ctx.guild.roles, id=self.config['SPECIAL_ROLE'])
		
		if member.top_role.position > special_role.position:
			nickname += ' ' + member.top_role.name.split(' ')[-1]

		nickname = nickname

		await member.edit(nick=nickname)
	

	@Cog.listener()
	async def on_member_update(self, before: Member, after: Member) -> None:
		
		if self.special_role == None:
			self.special_role = utils.get(after.guild.roles, id=int(self.config['SPECIAL_ROLE']))
		

		if before.top_role.name != after.top_role.name:

			display_name = after.display_name
			top_role_emoji = after.top_role.name.split(' ')[-1]
			display_name = deEmojify(display_name)

			if after.top_role.position >= self.special_role.position:
				display_name += ' ' + top_role_emoji

			
			await after.edit(nick=clean_name(display_name))

	
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot: commands.Bot):
	await bot.add_cog(Moderator(bot))
