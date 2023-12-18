# standard library imports
import asyncio
from datetime import datetime
import functools
from typing import Optional

# Third-party imports
from discord.ext import commands
from discord.ext.commands import Context, BadArgument

# Local application/library specific imports
from cores.database import Database
import cores.parameters as parameter
from cores.fantasy import Character
from cores.gambling import Slot, CoinFlip
from settings import CONFIG

class Gambling(commands.Cog, name="Gambling"):
    """
    **🎲 Gambling**
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

    @commands.hybrid_command(name="coin_flip",
                            description=CoinFlip.help(),
                            aliases=['cf']
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @ensure_user_exists
    async def coinflip(
        self, 
        context:Context, 
        bet = parameter.bet, 
        choice: Optional[str] = parameter.choice
    ):
        
        user = context.author
        user_id = user.id
        channel = context.channel

        data = self.supabase.select(user_id, 'character')
        character: Character = Character.from_json(data['character'])

        current_cash = character.infor.cash
       
        if current_cash == 0:
            raise BadArgument(f"{self.config['CASH_EMOJI']} | You have no money.")

        if bet > current_cash:
            bet = current_cash

        content = f"`BET` {bet} {self.config['CASH_EMOJI']}\n`CHOICE` {choice}\n`RESULT` "

        message = await channel.send(content + self.config['COIN_SPINS_EMOJI'])
        result = CoinFlip.play()
        if result == choice:
            character.infor.add_cash(bet)
            content += f"||{result}||\n{user.mention} ||win {bet:,}|| {self.config['CASH_EMOJI']}."
        else:
            character.infor.decrease_cash(bet)
            content += f"||{result}||\n{user.mention} ||lose {bet:,}|| {self.config['CASH_EMOJI']}."


        data['character'] = character.to_json()

        self.supabase.update(user_id, data)

        await asyncio.sleep(3)
        await message.edit(
            content = f"{content} Ur cash is ||{character.infor.cash:,}|| {self.config['CASH_EMOJI']}"
        )

    @commands.hybrid_command(name="slot",
                            description=Slot.help(),
                            aliases=['s']
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @ensure_user_exists
    async def slot(self, context:Context, bet = parameter.bet):
        
        user = context.author
        user_id = user.id

        data = self.supabase.select(user_id, 'character')
        character: Character = Character.from_json(data['character'])

        current_cash = character.infor.cash

        if bet > current_cash:
            bet = current_cash

        if bet == 0:
            raise BadArgument(f"{self.config['CASH_EMOJI']} | You have no money.")

        result = Slot.play()
        message = f"You bet {bet:,}. Result is {'|'.join(result)}."
        win = len(set(result)) == 1
        
        if win:
            character.infor.add_cash(bet * Slot.items[result[0]])
            await context.channel.send(content=message + f"\nYou win {bet:,}. {user.mention}, Ur cash is {character.infor.cash:,}")

        else:
            character.infor.decrease_cash(bet)
            await context.channel.send(content=message + f"\nYou lose {bet:,}. {user.mention}, Ur cash is {character.infor.cash:,}")

        data['character'] = character.to_json()

        self.supabase.update(user_id, data)
    

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Gambling(bot))