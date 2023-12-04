from discord.ext.commands import parameter

from cores.fantasy import Stat
from cores.converter import StatDisplayMode, PositiveInteger, MemberConverter


__all__ = (
    "stat",
    "display_mode",
    "spirit",
    "cash",
    "limit",
    "player"
)


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
    description="The amount of spirit to use for the upgrade."
)

cash = parameter(
    converter=PositiveInteger,
    description="The amount of cash to give."
)

limit = parameter(
    converter=PositiveInteger,
    description="The amount of messages to delete."
)

member = parameter(
    default=None,
    converter=MemberConverter,
    description="id or mention"
)

nickname = parameter(
    default=None,
    description="The new nickname."
)
