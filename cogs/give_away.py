

import asyncio
from datetime import datetime, timedelta
from random import choices


from discord import Embed
from discord.ext.commands import Context, Cog, Bot, hybrid_command, guild_only, has_role, bot_has_permissions

from cores.errors import ChannelError
from database.database import GiveAwayTable
import cores.parameters as parameter
from settings import CONFIG

class GiveAway(Cog, name="give away"):
	"""
	**🎉 Give away**
	It contains all the give away commands.
	"""
	def __init__(self, bot: Bot):
		self.bot = bot
		self.database = GiveAwayTable()
	
	
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
		
		access_channel = 1186268906361454614
		if ctx.channel.id != access_channel:
			raise ChannelError(f"You must use command at {ctx.guild.get_channel(access_channel).mention}")
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

		self.database.insert({
			'ga_id':msg.id,
			'channel_id':ctx.channel.id
		})

		await self.end_give_away(msg.id, ctx.channel.id)
		
	async def end_give_away(self, 
		ga_id, 
		channel_id,
	):
		try:
			channel = await self.bot.fetch_channel(channel_id)
			msg = await channel.fetch_message(ga_id)
		except Exception:
			return
		
		embed = msg.embeds[0]
		timestamps = int(embed.fields[2].value[3:-3])
		end_date = datetime.fromtimestamp(timestamps)
		await asyncio.sleep((end_date - datetime.now()).total_seconds())
		try:
			winners = int(embed.fields[1].value)
			users = {user.mention async for user in msg.reactions[0].users() if not user.bot}
			winners = choices(list(users), k = winners)
		except IndexError:
			embed.set_field_at(1, name="Winner(s): ", value="Nobody Join?", inline=False)
		except ValueError:
			self.database.delete(ga_id)
			return
		else:
			embed.set_field_at(1, name="Winner(s): ", value=', '.join(set(winners)), inline=False)
		await msg.edit(embed=embed)

		self.database.delete(ga_id)

async def setup(bot: Bot):
	await bot.add_cog(GiveAway(bot))