# standard library imports
import functools
from datetime import datetime
from typing import Optional

# Third-party imports
import discord
from discord.ext import commands
from discord.ext.commands import Context

# Local application/library specific imports
from cores.database import Database
import cores.parameters as parameter
from cores.fantasy import Character, FantasyWorld
from settings import CONFIG

class Game(commands.Cog, name="game"):
    """
    **🎮 Game**
    It contains all the RPG game commands.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """
        Initialize the Game cog with a bot, a database, and a fantasy world.
        :param bot: The bot client.
        """
        self.bot = bot
        self.config = CONFIG
        self.supabase = Database()
        self.world = FantasyWorld()
        

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
                
                success_emoji = message.guild.emojis.get(self.config['SUCCESS_EMOJI'])
                error_emoji = message.guild.emojis.get(self.config['ERROR_EMOJI'])

                await message.add_reaction(success_emoji)
                await message.add_reaction(error_emoji)

                valid_reactions = [success_emoji, error_emoji]

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
                             aliases=['p', 'me', 'info'],
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
            (self.config["HP_EMOJI"], current_stat.HP),
            (self.config["MP_EMOJI"], current_stat.MP),
            (self.config["STR_EMOJI"], current_stat.STR),
            (self.config["AGI_EMOJI"], current_stat.AGI),
            (self.config["PR_EMOJI"], current_stat.PR),
            (self.config["CR_EMOJI"], current_stat.CR)
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
                      stat:Optional[str] = parameter.stat, 
                      spirit:Optional[int] = parameter.spirit) -> None:
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

    @commands.hybrid_command(name="cash",
                            description="Show your cash",
                            aliases=['bal', 'balance', 'money'],
                            with_app_command=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    @ensure_user_exists
    async def cash(self, context: Context) -> None:
        """
        The cash command. It allows the user to see their cash.

        :param context: The application command context.
        :return: None
        """
        user = context.author
        data = self.supabase.select(user.id, 'character')
        player: Character = Character.from_json(data['character'])
        cash = player.infor.cash
        await context.channel.send(f"{self.config['CASH_EMOJI']} | You have {cash:,} cash.")
    

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Game(bot))
