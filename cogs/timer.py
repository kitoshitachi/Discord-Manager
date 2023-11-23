import datetime
from random import choice
from cores.database import Database
from discord.ext import commands, tasks
from discord import Client, CustomActivity, Status

# If no tzinfo is given then UTC is assumed.
class Timer(commands.Cog, name="timer"):
    def __init__(self, bot:Client):
        self.bot = bot
        self.database = Database()
        self.status_task.start()
        self.reset_limit.start()

    def cog_unload(self):
        self.my_task.cancel()

    @tasks.loop(time= datetime.time(hour=5, minute=0))
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

async def setup(bot) -> None:
    await bot.add_cog(Timer(bot))