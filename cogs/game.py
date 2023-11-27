# standard library imports
import functools
from datetime import datetime

# Third-party imports
import discord
from discord.ext import commands
from discord.ext.commands import Context

# Local application/library specific imports
from cores.database import Database
import cores.parameters as parameter
from cores.fantasy import Character, FantasyWorld

# External library
import yaml


class Game(commands.Cog, name="Game"):
    """
    A cog that represents a RPG game. It contains all the RPG game commands.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """
        Initialize the Game cog with a bot, a database, and a fantasy world.
        :param bot: The bot client.
        """
        self.bot = bot
        self.supabase = Database()
        self.world = FantasyWorld()
        self.config = self.load_config()

    def load_config(self):
        """
        Load the configuration from a YAML file.
        :return: The configuration.
        """
        try:
            with open('config.yml', 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print("Config file not found. Please ensure 'config.yml' exists.")
            return {}
        except yaml.YAMLError:
            print(
                "Error parsing config file. Please ensure 'config.yml' is a valid YAML file."
            )
            return {}

    def ensure_user_exists(func):
        """
        A decorator that ensures that the user exists in the database.
        :param func: The function to decorate.
        :return: The decorated function.
        """

        @functools.wraps(func)
        async def wrapper(self, context: Context, *args, **kwargs):
            user = context.author
            data = self.supabase.select(user.id, '*')
            if data is None:
                message = await context.channel.send(
                    'Agree to activate the system?')
                await message.add_reaction('✅')
                await message.add_reaction('❎')
                valid_reactions = ['✅', '❎']

                def check(reaction, user):
                    return user == context.author and str(
                        reaction.emoji) in valid_reactions

                reaction, user = await self.bot.wait_for('reaction_add',
                                                         timeout=30.0,
                                                         check=check)

                if str(reaction.emoji) == valid_reactions[0]:
                    new_member = {
                        'id': user.id,
                        'joined_date': str(datetime.now().date()),
                        'character': Character().to_json(),
                    }  # create new member data
                    self.supabase.insert(new_member)
                    await message.edit(content="Success!")
                else:
                    await message.edit(content="Cancelled!")
            return await func(self, context, *args, **kwargs)

        return wrapper

    @commands.hybrid_command(name="train",
                             description="Train to get exp, cash and random stat.\nYou can train 1000 times per day to get cash, stat and 3000 exp per day.",
                             aliases=['t'],
                             with_app_command=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    @ensure_user_exists
    async def train(self, context: Context) -> None:
        """
        The train command. It allows the user to train and get experience and stats.
        :param context: The application command context.
        :return: None
        """
        user = context.author
        data = self.supabase.select(user.id, '*')

        player: Character = Character.from_json(data['character'])

        xp, cash, stat_name, stat_increase, lvl_up = player.train(
            data['limit_xp'], data['status'])

        data['limit_xp'] -= xp
        data['status'] -= 1
        data['character'] = player.to_json()
        self.supabase.update(user.id, data)
        message = f"You have gained {xp} XP and {cash} cash. Your {stat_name} stat has increased to {stat_increase}."
        if lvl_up:
            message += " Congratulations, you have leveled up!"
        await context.channel.send(content=message, mention_author=True)

    #================== profile =========================

    @commands.hybrid_command(name='profile',
                             description="Show character's stats",
                             aliases=['stat'],
                             with_app_command=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @ensure_user_exists
    async def stat(self, context: Context) -> None:
        """
        The stat command. It allows the user to see their character's stats.

        :param context: The application command context.
        :return: None
        """
        user = context.author
        data = self.supabase.select(user.id, 'character')

        player: Character = Character.from_json(data['character'])

        embed = discord.Embed(title=f"{user.display_name}'s information",
                      color=0xFF7F7F)

        dashes = 8
        total_xp = player.infor.total_xp
        current_xp = player.infor.xp
        currentDashes = int(current_xp / int(total_xp / dashes))
        remainingDashes = dashes - currentDashes

        progressDisplay = '🟦' * currentDashes
        remainingDisplay = '⬛' * remainingDashes

        current_stat = player.stat
        max_len = len(str(current_stat.HP)) + 1

        embed.add_field(
            name=f"Level {player.infor.level} ({current_xp:,} / {total_xp:,} XP)",
            value=f"{progressDisplay}{remainingDisplay}",
            inline=False)

        stat_fields = [
            ("HP", current_stat.HP),
            ("MP", current_stat.MP),
            ("STR", current_stat.STR),
            ("AGI", current_stat.AGI),
            ("PR", current_stat.PR),
            ("CR", current_stat.CR)
        ]

        for name, value in stat_fields:
            embed.add_field(name=name, value=f"{value:0>{max_len}}", inline=True)

        embed.set_footer(text='Powered by Vampire')
        embed.set_thumbnail(url=user.display_avatar.url)
        await context.channel.send(embed=embed)

    @commands.hybrid_command(name='upgrade', 
                             description="Upgrade character's stats.\n", 
                             aliases=['up'],
                             with_app_command=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    @ensure_user_exists
    async def upgrade(self, context: Context, 
                      stat:str = parameter.stat, 
                      spirit:int = parameter.spirit) -> None:
        """
        The upgrade command. It allows the user to upgrade their character's stats.

        :param context: The application command context.
        :param stat: The stat to upgrade. Options are: HP, MP, STR, AGI, PR, CR.
        :param spirit: The amount of spirit to use for the upgrade.
        :return: None
        """

        user = context.author
        data = self.supabase.select(user.id, 'character')

        player: Character = Character.from_json(data['character'])
        msg = player.upgrade(stat, spirit)
        data['character'] = player.to_json()
        self.supabase.update(user.id, data)

        await context.channel.send(msg)


    
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Game(bot))
