"""
Define param
"""
from datetime import datetime
from typing import Optional

from discord.ext.commands import parameter

from core import Stat
from .converter import PositiveInteger, KeyAlias, TimeConverter
from settings import CONFIG


stat = parameter(
    converter=Stat,
    displayed_default='<stat>', 
    description="The stat to upgrade.\nOptions are: HP, MP, STR, AGI, PR, CR."
)

display_mode = parameter(
    default='display_stat',
    converter=KeyAlias(
        name='display profile mode',
        data=(
            ('display_stat', 'default', 'full', '0'),
            ('base_stat', 'base', '1'),
            ('bonus_stat', 'bonus', '2'),
            ('total_stat', 'total', '3')
        )
    ),
    description="The stat display mode to use.\
    \nOptions are:\
    \naliases `display stat`: 'default', 'full', '0'\
    \naliases `base stat`: 'base', '1'\
    \naliases `bonus stat`: 'bonus', '2'\
    \naliases `total stat`: 'total', '3'"
)


spirit: Optional[int]  = parameter(
    converter=PositiveInteger,
    description="The amount of spirit to upgrade."
)

cash: Optional[int]  = parameter(
    converter=PositiveInteger,
    description="The amount of cash to give"
)

limit: Optional[int] = parameter(
    converter=PositiveInteger(all=100),
    description="The amount of messages. Max is 100 per command"
)

bet: Optional[int] = parameter(
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

nickname:Optional[str] = parameter(
    description="The new nickname. If you dont write the name, then set ur name to guild name or clean username"
)

choice: Optional[str] = parameter(
    default=CONFIG['HEAD_COIN_EMOJI'],
    converter=KeyAlias
    (
        name='choice',
        data=(
            (CONFIG['HEAD_COIN_EMOJI'],'head','h'), 
            (CONFIG['TAIL_COIN_EMOJI'],'tail','t')
        )
    ),
    description="choose face of coin"
)

time: datetime = parameter(
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