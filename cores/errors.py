from typing import Any
from discord.ext.commands import CommandError
class ChannelError(CommandError):

    def __init__(self, message: str | None = None, *args: Any) -> None:
        if message is not None:
            super().__init__(message, *args)
        else:
            super().__init__(*args)