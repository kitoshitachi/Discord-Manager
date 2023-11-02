""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
import json, yaml

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from classes.database import Database
from classes.errors import DataNotFound
from classes.fantasy import Character, FantasyWorld
# Here we name the cog and create a new class for the cog.
class Game(commands.Cog, name="rpg game"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.supabase = Database()
        self.world = FantasyWorld()
        with open('config.yml','r') as f:
            self.config = yaml.safe_load(f)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="train",
        description="train to get exp and stat",
        aliases=['t']
    )
    @commands.cooldown(1, 15,commands.BucketType.user)
    async def train(self, context: Context) -> None:
        """
        :param context: The application command context.
        """       
        user = context.author
        data = self.supabase.select(user.id,'*')
        
        if data == None:
            raise DataNotFound
        

        player:Character = json.loads(data['character'])
        
        xp, cash, stat, msg = player.train(data['limit_xp'], data['status'])
        
        data['limit_xp'] -= xp
        data['status'] -= 1

        data['character'] = json.dumps(player)

        if self.supabase.update(user.id, data):
            message = [
                f"| {user.display_name}, you got **{xp} exp** and **{cash:,} Bloody Coins** ||",
                '| '.join([f'{stat_name}: + {value}' for stat_name, value in stat.items()])

            ]
            await context.channel.send('\n'.join(message) + msg if msg is not None else '')
        else:
            await context.channel.send(f"something wrong ! {data}")

    #================== profile =========================

    @commands.hybrid_command(
        name='profile',
        description =  'Show profile',
    )
    @commands.cooldown(1,30,commands.BucketType.user)
    async def stat(self, context:Context) -> None:
        user = context.author
        data = self.supabase.select(user.id, 'character')

        if data == None:
            raise DataNotFound
        
        character:Character = json.loads(data['character'])
 
        embed = Embed(title=f"{user.display_name}'s information", 
                      description=character.stat())
        
        dashes = 5
        total_xp = character.infor.total_xp
        current_xp = character.infor.xp
        dashConvert = int(total_xp / dashes)
        currentDashes = int(current_xp / dashConvert)
        remainingDashes = dashes - currentDashes

        progressDisplay = '🟦' * currentDashes
        remainingDisplay = '⬛' * remainingDashes

        embed.add_field(name=f"Level {character.infor.level} ({current_xp:,} / {total_xp:,} xp)", value=f"{progressDisplay}{remainingDisplay}", inline=False)

        embed.set_footer(text='Powered by Vampire')
        embed.set_thumbnail(url=user.avatar.url)
        await context.channel.send(embed=embed)


    @commands.hybrid_command(
        name='add',
        description =  'Add stat',
    )
    @commands.cooldown(1,15,commands.BucketType.user)
    async def add(self, context:Context, stat:str, spirit:int) -> None:
        user = context.author
        data = self.supabase.select(user.id, 'character')

        if data == None:
            raise DataNotFound
        
        character:Character = json.loads(data['character'])
        msg = character.upgrade(stat, spirit)

        self.supabase.update(user.id, json.dumps(character))

        await context.channel.send(msg)

        pass    

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Game(bot))