from datetime import datetime, timedelta
import re

from discord.ext.commands import ( 
    Context, Converter, BadArgument
)
    
class PositiveInteger(Converter):
    '''
    Converts to a positive integer.
    if all is not given then 'all' is returned
    '''
    def __init__(self, all = None) -> None:
        super().__init__()
        self.all = all or 'all'

    async def convert(self, ctx: Context, argument: str) -> int:
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
    default is 1st key
    return first item of tuple as full content    
    '''

    def __init__(self, name, data:list) -> None:
        super().__init__()
        self.name = name
        self.list_of_keys = data
        self.default = data[0][0]

    @property
    def list_option(self):
        return ", ".join([" = ".join(key_alias) for key_alias in self.list_of_keys])

    async def convert(self, ctx: Context, argument: str):

        for key_alias in self.list_of_keys:
            if argument in key_alias:
                return key_alias[0]
        
        raise BadArgument(f"{argument} is invalid. Optional {self.name}: {self.list_option}")

class TimeConverter(Converter):

    def __init__(self,min_second:int = 15, max_second:int = 24 * 60 * 60) -> None:
        super().__init__()
        self.max_second = max_second
        self.min_second = min_second


    async def convert(self, ctx: Context, argument):
        time_dict = self.extract_time_values(argument)
        time_delta = self.to_timedelta(*time_dict.values())
        total_seconds = time_delta.total_seconds()

        if total_seconds > self.max_second or total_seconds < self.min_second:
            raise BadArgument(f"{argument} is invalid. time in range [{self.min_second},{self.max_second}] seconds")

        return datetime.now() + time_delta

    @staticmethod
    def to_timedelta(days:int, hours:int, minutes:int, seconds:int):
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def extract_time_values(input_string:str):
        time_dict = {'d': 0, 'h':0, 'm':0, 's':0}
        items = re.finditer(r'(\d+(\.\d+)?)([smhd])', input_string.lower())
        
        for match in items:
            value = float(match.group(1))
            unit = match.group(3)
            time_dict[unit] = value

        return time_dict
