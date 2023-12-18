import datetime
import asyncio

from random import choice
from cores.database import Database
from discord.ext import commands, tasks
from discord import Client, CustomActivity, Status

from cogs.give_away import GiveAway
# If no tzinfo is given then UTC is assumed.
class Timer(commands.Cog, name="timer"):
    """
    A cog that represents a timer. It contains all the timer commands.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Database()
        self.give_away = GiveAway(bot)
        self.status_task.start()
        self.reset_limit.start()
        self.check_give_away.start()
        self.my_task = None

    def cog_unload(self):
        '''
        Cancel the task when the cog is unloaded.
        '''
        self.my_task.cancel()

    @tasks.loop(time=datetime.time(hour=5, minute=0))
    async def reset_limit(self):
        self.database.reset_limit()

    @tasks.loop(hours=8.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        Activities = [
            CustomActivity(name="Drinking !", emoji='🍷'),
            CustomActivity(name="Fighting !", emoji='⚔️'),
            CustomActivity(name="Sleeping !", emoji='⚰️'),
        ]
        await self.bot.change_presence(status=Status.online,
                                       activity=choice(Activities))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        await self.bot.wait_until_ready()


    @tasks.loop(count=1)
    async def check_give_away(self) -> None:
        records = self.database.select_all_ga()
        asyncio.gather(*[self.give_away.end_give_away(data['ga_id'], data['channel_id']) for data in records])
        
        
        


async def setup(bot) -> None:
    await bot.add_cog(Timer(bot))
