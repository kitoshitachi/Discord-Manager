# standard library imports
import functools
from datetime import datetime
from typing import Optional
from io import BytesIO

# Third-party imports
from discord import Member, Embed, File
from discord.ext import commands
from discord.ext.commands import Context

# Local application/library specific imports
from cores.card import Card
from cores.database import Database
import cores.parameters as parameter
from cores.fantasy import Character, Stat
from cores.gambling import Slot, CoinFlip
from settings import CONFIG

class Game(commands.Cog, name="game"):
    """
    **<:game:1181633887978389524> Game**
    It contains all the RPG game commands.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """
        The constructor for the Game class.
        :param bot: The bot client.
        """
        self.bot = bot
        self.config = CONFIG
        self.supabase = Database()
        self.card = Card()
        

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
                
                success_emoji = self.config['SUCCESS_EMOJI']
                error_emoji = self.config['ERROR_EMOJI']

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
                             aliases=['t'])
    # @commands.group(name='RPG')
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
                             aliases=['me', 'info'])
    # @commands.group(name='RPG')
    @commands.cooldown(1, 15, commands.BucketType.user)
    @ensure_user_exists
    async def profile(self, context: Context, mode:str = parameter.display_mode) -> None:
        """
        The stat command. It allows the user to see their character's stats.

        :param context: The application command context.
        :return: None
        """
        user = context.author
        data = self.supabase.select(user.id, 'character')

        player: Character = Character.from_json(data['character'])

        name=user.display_name
        avatar = await user.avatar.read()
        image = self.card.image(name, player, mode, avatar)

        with BytesIO() as binary_image:
            image.save(binary_image, format="PNG")
            binary_image.seek(0)
            await context.channel.send(file=File(fp=binary_image, filename="Profile.png"))


        # await context.channel.send(embed=embed)

    @commands.hybrid_command(name='upgrade', 
                             description="Upgrade character's stats.\n", 
                             aliases=['up'])
    # @commands.group(name='RPG')
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
                            aliases=['bal', 'balance', 'money'])
    # @commands.group(name='RPG')
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
    
    @commands.hybrid_command(name="give",
                            description="Give cash to another user",
                            aliases=['transfer'])
    # @commands.group(name='RPG')
    @commands.cooldown(1, 15, commands.BucketType.user)
    @ensure_user_exists
    async def give(self, context: Context, 
                   other: Optional[Member], 
                   cash: Optional[str] = parameter.cash) -> None:
        """
        The give command. It allows the user to give cash to another user.

        :param context: The application command context.
        :param user: The user to give cash to.
        :param cash: The amount of cash to give.
        :return: None
        """
        
        if other == context.author:
            await context.channel.send("You give cash to yourself.")
            return


        other_id = other.id
        author_id = context.author.id

        other_player_data = self.supabase.select(other_id, 'character')
        if other_player_data is None:
            await context.channel.send("User not found.")
            return
        
        author_data = self.supabase.select(author_id, 'character')

        other_player: Character = Character.from_json(other_player_data['character'])
        author_player: Character = Character.from_json(author_data['character'])

        if cash == 'all':
            cash = author_player.infor.cash

        if author_player.infor.cash < cash:
            await context.channel.send("You don't have enough cash.")
            return
        
        other_player.infor.add_cash(cash)
        author_player.infor.decrease_cash(cash)

        other_player_data['character'] = other_player.to_json()
        author_data['character'] = author_player.to_json()

        self.supabase.update(other_id, other_player_data)
        self.supabase.update(author_id, author_data)

        await context.channel.send(f"You give {cash:,} cash to {other.mention}.")

    @commands.hybrid_command(name="limit",
                            description="Show limit train and xp",
                            # aliases=['']
    )
    # @commands.group(name='RPG')
    @commands.cooldown(1, 15, commands.BucketType.user)
    @ensure_user_exists
    async def limit(self, context:Context):

        user = context.author
        data = self.supabase.select(user.id, 'status, limit_xp')
        
        embed = Embed(title="Today's Limit")
        embed.add_field(name='Train', value=f'{data["status"]} times to increase stat', inline=False)
        embed.add_field(name='Exp', value=f'{data["limit_xp"]} XP remaining', inline=False)
        embed.set_footer(text='Powered by Vampire')
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await context.channel.send(embed=embed)

    @commands.hybrid_command(name="coinflip",
                            description="coinflip game",
                            aliases=['cf']
    )
    # @commands.group(name='Gambling')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @ensure_user_exists
    async def coinflip(self, 
                       context:Context, 
                       bet = parameter.bet, 
                       choice: Optional[str] = parameter.choice):
        
        user_id = context.author.id

        data = self.supabase.select(user_id, 'character')
        character: Character = Character.from_json(data['character'])

        current_cash = character.infor.cash

        if bet > current_cash:
            bet = current_cash

        win = CoinFlip.play(choice)
        if win:
            character.infor.add_cash(bet)
            await context.channel.send(content=f"You win {bet:,}. Ur cash is {character.infor.cash:,}")

        else:
            character.infor.decrease_cash(bet)
            await context.channel.send(content=f"You lose {bet:,}. Ur cash is {character.infor.cash:,}")

        data['character'] = character.to_json()

        self.supabase.update(user_id, data)

    

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Game(bot))
