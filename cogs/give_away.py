

import asyncio
from datetime import datetime
from random import choices
from discord import Embed
from discord.ext.commands import Context, Cog, Bot, hybrid_command, guild_only, has_role, bot_has_permissions

import cores.parameters as parameter
from settings import CONFIG

class GiveAway(Cog, name="give away"):
	"""
	**🎉 Give away**
	It contains all the give away commands.
	"""
	def __init__(self, bot: Bot):
		self.bot = bot
	
	
	@hybrid_command(
		name="give_away",
		description="create a give away",
		aliases = ['ga','giveaway']
	)
	@guild_only()
	@has_role(1179428320501301419)
	@bot_has_permissions(manage_messages=True)
	async def give_away(self, 
		ctx: Context, 
		time = parameter.time, 
		winner = parameter.winner,
		*,
		prize = parameter.prize,
	):
		embed = Embed(title=f"{ctx.author.display_name} 's Give Away", color = CONFIG['RED'], timestamp=time)
		embed.add_field(name="Prize: ", value=prize, inline=False)
		embed.add_field(name="Winner(s): ", value=winner, inline=False)
		embed.add_field(name="End at: ", value=f"<t:{int(time.timestamp())}:R>", inline=False)
		embed.set_thumbnail(url=ctx.author.avatar.url)
		embed.set_footer(text='Powered by Vampire')

		await ctx.message.delete()

		msg = await ctx.channel.send(embed=embed)
		invalid_emoji = '🎉'
		await msg.add_reaction(invalid_emoji)
		await asyncio.sleep((time - datetime.now()).total_seconds())

		msg = await ctx.fetch_message(msg.id)
		try:
			users = {user.mention async for user in msg.reactions[0].users() if not user.bot}
			winners = choices(list(users), k = winner)
		except IndexError:
			embed.set_field_at(1, name="Winner(s): ", value="Nobody Join?", inline=False)
		else:
			embed.set_field_at(1, name="Winner(s): ", value=', '.join(set(winners)), inline=False)
		await msg.edit(embed=embed)

async def setup(bot: Bot):
	await bot.add_cog(GiveAway(bot))