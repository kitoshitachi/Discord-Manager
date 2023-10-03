""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
import json
from math import ceil
import yaml
from discord.ext import commands
from discord.ext.commands import Context
from classes.database import Database
from classes.fantasy import FantasyWorld
from classes.utils import create_member
# Here we name the cog and create a new class for the cog.
class Character(commands.Cog, name="character"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.supabase = Database()
        self.world = FantasyWorld()
        with open('config.yml','r') as f:
            self.config = yaml.safe_load(f)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="steal",
        description="steal to get exp and items",
        aliases=['s']
    )
    @commands.cooldown(1,20,commands.BucketType.user)
    async def steal(self, context: Context) -> None:
        """
        hunt animals get items and 0.001 or 0.002 agi stat
        0.0001% get 1 stat crit
        :param context: The application command context.
        """
        await self.__update_data__(context, 'agi', 'crit')
            
        pass

    @commands.hybrid_command(
        name="hunt",
        description="hunt to get exp and items",
        aliases=['h']
    )
    @commands.cooldown(1,20,commands.BucketType.user)
    async def hunt(self, context: Context) -> None:
        """
        hunt animals get items and 0.001 or 0.002 agi stat
        0.0001% get 1 stat crit
        :param context: The application command context.
        """
        await self.__update_data__(context, 'str', 'def')
            
        pass

    async def __update_data__(self, context:Context, stat_name:str=None, luck_stat_name:str=None ) -> None:        
        user = context.author
        data = self.supabase.get(user.id)
        if data is None:
            await create_member(self.bot, self.supabase, context, user.id)
            return True
        xp, cash, stat_bonus, luck_stat = self.world.get_items()

        data['cash'] += cash
        data['limit_work'] -= 1
        stat = json.loads(data['character'])
        stat[stat_name] += stat_bonus
        stat[luck_stat_name] += luck_stat

        total_xp = ceil( data['level'] / self.config['X'] ) ** self.config['Y']
        print(f"X:{self.config['X']}")
        print(f"Y:{self.config['Y']}")
        print(f"total xp: {total_xp}")
        if data['limit_experience'] < xp:
            xp = data['limit_experience']
        current_xp = xp + data['experience']
        data['limit_experience'] -= xp
        #level up
        if current_xp >= total_xp:
            data['level'] += 1
            data['experience'] -= total_xp

            stat['spirit'] += self.config['STAT_PER_LEVEL']
        else:
            data['experience'] = current_xp
        
        data['character'] = json.dumps(stat)
        if self.supabase.update(user.id, data):
            await context.channel.send(f"| {user.display_name}, you got **{xp} exp** and **{cash:,} Bloody Coins**. \
                                  \n| Stat increase {stat_name.upper()}:{stat_bonus} " + (f" and {luck_stat_name.upper()}: {luck_stat}!" if luck_stat else "!") )
        else:
            await context.channel.send(f"something wrong ! {data}")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Character(bot))