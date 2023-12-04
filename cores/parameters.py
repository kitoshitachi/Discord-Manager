"""
Define param
"""

from discord.ext.commands import parameter

from cores.fantasy import Stat
from cores.converter import StatDisplayMode, PositiveInteger, KeyToIndex

stat = parameter(
    converter=Stat, 
    description="The stat to upgrade.\nOptions are: HP, MP, STR, AGI, PR, CR."
)

display_mode = parameter(
    default="display_stat",
    converter=StatDisplayMode,
    description="The stat display mode to use.\
    \nDefault is 0, which is `display_stat`.\
    \nOptions are:\
    \n0: `display stat`\
    \n1: `base stat`\
    \n2: `bonus stat`\
    \n3: `total stat`"
)


spirit = parameter(
    converter=PositiveInteger,
    description="The amount of spirit to upgrade."
)

cash = parameter(
    converter=PositiveInteger,
    description="The amount of cash to give"
)

limit = parameter(
    converter=PositiveInteger(all=100),
    description="The amount of messages. Max is 100 per command"
)

bet = parameter(
    default=1,
    converter=PositiveInteger(all=250000),
    description='The amount of cash to bet. \
    \nMax is 250000 per command\
    \nDefault is 1'
)

nickname = parameter(
    default=None,
    description="The new nickname."
)

choice = parameter(
    default='head',
    converter=KeyToIndex
    (
        [
            ['head','h'],
            ['tail','t']    
        ]    
    ),
    description="choose face of coin"
)