
from discord.ext.commands import ( 
    Context, 
    Converter, FlagConverter, 
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
    def __init__(self, all = None) -> None:
        super().__init__()
        self.all = all or 'all'

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
                return self.all
            number = int(argument)
            if number <= 0:
                raise BadArgument(f"{argument} must be a positive integer.")
            return number
        except ValueError:
            raise BadArgument(f"{argument} invalid. Must be a positive integer.")


class KeyAlias(Converter):
    '''
    convert the flag to full content name
    Data schema  = (tuple of 1st key alias, tuple of 2nd key alias,...)

    return first item of tuple as full content    
    '''

    def __init__(self, name, data:list) -> None:
        super().__init__()
        self.name = name
        self.list_of_keys = data

    @property
    def list_option(self):
        return ", ".join([option for key_alias in self.list_of_keys for option in key_alias])

    async def convert(self, ctx: Context, argument: str):

        for key_alias in self.list_of_keys:
            if argument in key_alias:
                return key_alias[0]
        
        raise KeyError(f"{argument} is invalid. Optional {self.name}: {self.list_option}")
