import re
from typing import Optional

from discord import HTTPException, Member, Guild
import discord
from discord.ext.commands import ( 
    Context, Bot, 
    Converter, FlagConverter, IDConverter,
    BadArgument, BadArgument
)

class StatDisplayMode(FlagConverter):
    def __init__(self) -> None:
        super().__init__()

        self._mode = ['display_stat', 'base_stat', 'bonus_stat', 'total_stat']

    async def convert(self, ctx: Context, argument: str) -> str:
        '''
        Converts to a stat display mode.

        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context that triggered this converter.
        argument: :class:`str`
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
        id = int(argument)
        if id in range(4):
            return self._mode[id]
        else:
            raise BadArgument(f"{argument} is not a valid display mode. Options are: {', '.join(self._mode)}")
        
    
class PositiveInteger(Converter):
    '''
    Converts to a positive integer.
    '''

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

class MemberConverter(IDConverter[Member]):
    """
    Converts to a :class:`~discord.Member`.
    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.

    All lookups are done via the :attr:`~discord.Client.guilds` cache.

    Special case for my bot: if the member is not found, return the argument

    """

    async def query_member_by_id(self, bot: Bot, guild: Guild, user_id: int) -> Optional[Member]:
        """
        Queries the member from the ID provided.
        This is done by first checking the cache, if it isn't found then it
        will then check the HTTP API.
        Parameters
        -----------
        bot: :class:`Bot`
            The bot that is doing the querying.
        guild: :class:`Guild`
            The guild that we are getting the member from.
        user_id: :class:`int`
            The user ID to query with.
        Returns
        --------
        Optional[:class:`Member`]
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

    

    async def convert(self, ctx: Context, argument: str):
        """
        Converts to a :class:`~discord.Member`.
        The lookup strategy is as follows (in order):
        1. Lookup by ID.
        2. Lookup by mention.
        
        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context that triggered this converter.
        argument: :class:`str`
            The argument that is being converted.

        Returns
        --------
        Optional[:class:`Member`]
            The member or argument if not found.
        """
        if argument == '':
            return argument

        bot = ctx.bot
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]{15,20})>$', argument)
        guild = ctx.guild
        result = None
        user_id = None

        if match:
            user_id = int(match.group(1))
            result = guild.get_member(user_id)

        if not isinstance(result, Member) and guild and user_id:
            result = await self.query_member_by_id(bot, guild, user_id)

        if result is None:
            return argument
        
        return result
    