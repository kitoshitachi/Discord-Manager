""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from supabase import create_client, Client
from settings import SUPABASE_URL, SUPABASE_KEY
from discord import Embed, Color
                


# Here we name the cog and create a new class for the cog.
class Gambling(commands.Cog, name="gambling"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    async def __init_member(self, context:Context, _id:int) -> None:
        """
        create new member data
        """

        message = await context.channel.send('Agree to activate the system?')
        await message.add_reaction('✅')
        await message.add_reaction('❎')
        valid_reactions = ['✅', '❎']
        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in valid_reactions
        
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

        if str(reaction.emoji) == valid_reactions[0]:
            data, count = self.supabase.table('Member') \
                .insert(
                    {'id':_id, 
                     'joined_date': str(datetime.now().date())}
            ).execute()
            await message.edit(content="Success!")
        else:
            await message.edit(content="Cancelled")


    @commands.hybrid_command(
        name="cash",
        description="Show ur cash",
    )
    @commands.command(aliases=['bal'])
    async def cash(self, context: Context) -> None:
        """
        show cash.

        :param context: The application command context.
        """
        id = context.author.id
        data, count = self.supabase.from_('Member') \
            .select('cash') \
            .eq('id', id) \
            .execute()
        if data[1] == []:
            await self.__init_member(context, id)
        else:
            data = data[1][0]
            await context.channel.send(f"💰{context.message.author.display_name}, you currently have **{data['cash']} Bloody Coins**!")

    @commands.hybrid_command(
        name="level",
        description="Show ur profile",
    )
    @commands.command(aliases=['lvl','xp'])
    async def level(self, context: Context) -> None:
        """
        show cash.

        :param context: The application command context.
        """
        id = context.author.id
        data, count = self.supabase.from_('Member') \
            .select('level, experience') \
            .eq('id', id) \
            .execute()
        if data[1] == []:
            await self.__init_member(context, id)
        else:
            data = data[1][0]
            user = context.author
            embed = Embed(title=user.display_name)
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name='color',value=Color.red())
            embed.add_field(name="Level:", value=f"{data['level']:,}")
            await context.channel.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Gambling(bot))