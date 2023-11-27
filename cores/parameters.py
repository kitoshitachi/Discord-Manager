from discord.ext import commands
from cores.fantasy import Stat
__slots__ = ["Stat", "Spirit"]

stat = commands.parameter(converter=Stat, description="The stat to upgrade.\nOptions are: HP, MP, STR, AGI, PR, CR.")
spirit = commands.parameter(description='The amount of spirit to use for the upgrade.')