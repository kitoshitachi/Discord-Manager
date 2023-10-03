""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

from random import randint
import yaml
from math import ceil
from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed, Color
from classes.database import Database                
from classes.utils import create_member

# Here we name the cog and create a new class for the cog.
class Gambling(commands.Cog, name="gambling"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.supabase = Database()
        with open('config.yml','r') as f:
            self.config = yaml.safe_load(f)

    @commands.hybrid_command(
        name="cash",
        description="Show ur cash",
        aliases=['bal']
    )
    async def cash(self, context: Context) -> None:
        """
        show cash.

        :param context: The application command context.
        """
        user = context.author        
        data = self.supabase.get(user.id, "cash")

        if data is None:
            await create_member(self.bot, self.supabase, context, user.id)
            return


        await context.channel.send(f"💰{context.message.author.display_name}, you currently have **{data['cash']:,} Bloody Coins**!")

    @commands.hybrid_command(
        name="level",
        description="Show ur profile",
        aliases=['lvl','xp']
    )
    async def level(self, context: Context) -> None:
        """
        show cash.

        :param context: The application command context.
        """
        user = context.author
        data = self.supabase.get(user.id,'level, experience')
        if data is None:
            await create_member(self.bot, self.supabase, context, user.id)
            return


        embed = Embed(title=f"{user.display_name}'s Information", color=Color.red())
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Role", value=user.top_role.name)
        dashes = 10
        total_xp = ceil( data['level'] / self.config['X'] ) ** self.config['Y']

        dashConvert = int(total_xp / dashes)
        currentDashes = int(data['experience'] / dashConvert)
        remainingDashes = dashes - currentDashes

        progressDisplay = '🟦' * currentDashes
        remainingDisplay = '⬛' * remainingDashes

        embed.add_field(name=f"Level {data['level']} ({data['experience']:,} / {total_xp:,} xp)", value=f"{progressDisplay}{remainingDisplay}", inline=False)
        embed.set_footer(text="Powered by Vampire")
        await context.channel.send(embed=embed)

    # @commands.hybrid_command(
    #     name='flip',
    #     description="gamble coin flip",
    #     aliases=['cf']
    # )
    # async def flip(self, context:Context, flag:str = 't 1') -> None:
    #     flag = flag.split(' ')
    #     if len(flag) > 2:
    #         raise commands.BadArgument('Wrong syntax!')
        
    #     if flag[0] == 'all':
    #         bet = 250000
    #         choice = flag[1]
    #     elif flag[1] == 'all':
    #         bet = 250000
    #         choice = flag[0]
    #     elif flag[0].isdecimal():
    #         bet = flag[0]
    #         choice = flag[1]
    #     elif flag[1].isdecimal():
    #         bet = flag[1]
    #         choice = flag[0]
    #     else:
    #         raise commands.BadArgument('Wrong syntax!')


    #     if choice in ['t','tail']:
    #         choice = 1
    #     elif choice in ['h','head']:
    #         choice = 0
    #     else:
    #         raise commands.BadArgument('Wrong syntax!')

    #     user = context.author
    #     error, data = self.check_bet(user.id, bet)
    #     if error is True:
    #         await context.channel.send(f"{user.mention}, **you don't have enough Bloody Coins!**",delete_after=10.)
    #     else:
    #         result = randint(0,1)
    #         if result == choice:
    #             data['cash'] += bet
    #             await context.channel.send(f"{user.mention}, you won **{bet:,} Bloody Coins!**")
    #         else:
    #             data['cash'] -= bet
    #             await context.channel.send(f"{user.mention}, you lost **{bet:,} Bloody Coins!**")
            
    #         self.supabase.update(user.id, data)
        
        
    #     pass

    # def check_bet(self, id:int, bet:int):
    #     data = self.supabase.get(id,'cash')
    #     return bool(data['cash'] < bet), data
        


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Gambling(bot))