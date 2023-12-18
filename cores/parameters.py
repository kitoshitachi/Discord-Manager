"""
Define param
"""
from datetime import datetime

from discord.ext.commands import parameter

from cores.fantasy import Stat
from cores.converter import StatDisplayMode, PositiveInteger, KeyAlias, TimeConverter
from settings import CONFIG

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
    \nMax is 250,000 per command\
    \nDefault is 1'
)

winner:int = parameter(
    converter=PositiveInteger(all=10),
    description="The amount of winner. \
    \nMax is 10\nMin is 1"
)

nickname:str = parameter(
    default=None,
    description="The new nickname. If you dont write the name, then set ur name to guild name or clean username"
)

choice = parameter(
    default=CONFIG['HEAD_COIN_EMOJI'],
    converter=KeyAlias
    (
        name='choice',
        data=((CONFIG['HEAD_COIN_EMOJI'],'head','h'), (CONFIG['TAIL_COIN_EMOJI'],'tail','t'))),
    description="choose face of coin"
)

time:datetime = parameter(
    converter=TimeConverter,
    description="Set time end give away. \
        \nMax is 1 day \
        \nMin is 15 seconds \
        \nFormat: **nd nh nm ns** with n is number \
        \nExample: 15s, 1d1h, ..."
)

prize:str = parameter(
    description="The prize of give away."
)