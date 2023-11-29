import re
from typing import Optional
from discord import Guild, HTTPException, Member, utils
from discord.ext.commands import ( 
    Context, Bot, parameter,
    Converter, IDConverter, FlagConverter,
    BadArgument, MemberNotFound, BadArgument
)

from cores.fantasy import Stat
__slots__ = ["Stat", "Spirit"]

class StatDisplayMode(FlagConverter):
    def __init__(self) -> None:
        super().__init__()
        display_mode = ["display_stat", "display", "0"]
        base_mode = ["base_stat", "base", "1"]
        bonus_mode = ["bonus_stat", "bonus", "2"]
        total_mode = ["total_stat", "total", "3"]

        self._mode = {
            "display_stat": display_mode,
            "base_stat": base_mode,
            "bonus_stat": bonus_mode,
            "total_stat": total_mode
        }

    async def convert(self, ctx: Context, argument: str) -> str:
        '''
        Converts to a stat display mode.

        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context that triggered this converter.
        argument: :class:`str`. if argument is None, `display_stat` is returned.
            The argument that is being converted.

        Raises
        -------
        :exc:`BadArgument`
            If the argument could not be converted into a stat display mode.

        Returns
        --------
        :class:`str`
            The stat display mode that was requested.

        '''
        if argument is None:
            return 'display_stat'

        argument = argument.lower()
        for key in self._mode.keys():
            if argument in self._mode[key]:
                return key
        
        raise BadArgument(f"{argument} is not a valid stat display mode. Options are: {', '.join(self._mode.keys())}")
        
    
class PositiveInteger(Converter):
    def __init__(self, *, minimum: int = 0, maximum: Optional[int] = None):
        self.minimum = minimum
        self.maximum = maximum
        

    async def convert(self, ctx: Context, argument: str):
        '''
        Converts to a positive integer.
        
        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context that triggered this converter.
            argument: :class:`str`
            The argument that is being converted.
            Raises
            -------
            :exc:`BadArgument`
            If the argument could not be converted into a positive integer.
            Returns
            --------
            :class:`int`
            The positive integer that was requested.
        '''
        try:
            if argument.lower() == "all":
                return "all"
            number = int(argument)
            if number < 0:
                raise BadArgument(f"{argument} must be a positive integer.")
            return number
        except ValueError:
            raise BadArgument(f"{argument} invalid. Must be a positive integer.")

class PlayerConverter(IDConverter[Member]):
    """
    Converts to a :class:`~discord.Member` or `~discord.User`.
    All lookups are via the local guild cache.
    The lookup strategy is as follows (in order):
    1. Lookup by mention.
    2. Lookup by ID.
    """

    async def query_member_by_id(self, bot: Bot, guild: Guild, user_id: int) -> Optional[Member]:
        """|coro|
        Retrieves a :class:`~discord.Member` from an ID.
        This is done by first checking the guild cache. If it isn't found then
        it fetches them from the API.
        Parameters
        -----------
        bot: :class:`Bot`
            The bot that relates to the member.
        guild: :class:`Guild`

        user_id: :class:`int`
            The member's ID to fetch from.
        Raises
        -------
        :exc:`HTTPException`
            Getting the member failed.
        Returns
        --------
        Optional[:class:`~discord.Member`]
            The member or ``None`` if not found.
        """

        ws = bot._get_websocket(shard_id=guild.shard_id)
        cache = guild._state.member_cache_flags.joined
        if ws.is_ratelimited():
            # If we're being rate limited on the WS, then fall back to using the HTTP API
            # So we don't have to wait ~60 seconds for the query to finish
            try:
                member = await guild.fetch_member(user_id)
            except HTTPException:
                return None

            if cache:
                guild._add_member(member)
            return member

        # If we're not being rate limited then we can use the websocket to actually query
        members = await guild.query_members(limit=1, user_ids=[user_id], cache=cache)
        if not members:
            return None
        return members[0]

    async def convert(self, ctx: Context[Bot], argument: str) -> Member:
        '''Converts to a :class:`~discord.Member` or `~discord.User`.
        All lookups are via the local guild cache.
        The lookup strategy is as follows (in order):
        1. Lookup by mention.
        2. Lookup by ID.
        
        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context that triggered this converter.
        argument: :class:`str`
            The argument that is being converted.
        
        Raises
        -------
        :exc:`BadArgument`
            If the argument could not be converted into a :class:`~discord.Member` or `~discord.User`.
        :exc:`MemberNotFound`
            If the member being converted could not be found.
        :exc:`HTTPException`
            Getting the member failed.
        Returns
        --------
        :class:`~discord.Member` or `~discord.User`
            The member or user that was requested.
        '''

        if ctx.message.mentions:
            if ctx.message.mentions[0]:
                return ctx.message.mentions[0]
        
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
        bot = ctx.bot
        guild = ctx.guild

        if match:
            member_id = int(match.group(1))
            member = utils.get(guild.members, id=member_id)

        if member is None or not isinstance(member, Member):
            if guild is None or member_id is None:
                raise MemberNotFound(argument)
            member = await self.query_member_by_id(bot , guild, member_id)
            if member is None:
                raise MemberNotFound(argument)

        return member



stat = parameter(
    converter=Stat, 
    description="The stat to upgrade.\nOptions are: HP, MP, STR, AGI, PR, CR."
)

display_mode = parameter(
    converter=StatDisplayMode,
    description="The stat display mode to use.\
    \nDefault is display mode.\
    \nOptions are: 0, 1, 2, 3\
    \n0 (aliases: display_stat, display)\
    \n1 (aliases: base_stat, base)\
    \n2 (aliases: bonus_stat, bonus)\
    \n3 (aliases: total_stat, total)"
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

player = parameter(
    converter=PlayerConverter,
    description="id or mention"
)


