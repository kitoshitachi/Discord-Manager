from typing import List, Mapping, Optional
import discord

from discord.ext import commands
from discord.ext.commands import Cog, Command
from cores.view import PaginationView

from settings import PREFIX_BOT

class CustomHelpCommand(commands.HelpCommand):
    '''
    A custom help command for the Discord bot.

    '''
    def get_command_signature(self, command: Command):
        return f"{self.context.clean_prefix} {command.name} {command.signature}"

    async def send_bot_help(self, mapping:Mapping[Optional[Cog], List[Command]]):
        
        pages = []

        for cog, commands in mapping.items():
            if cog is None:
                continue
            filtered_commands = await self.filter_commands(commands, sort=True)
            command_names = [command.name for command in filtered_commands]
            if command_names:
                cog_name = cog.qualified_name.replace(" ", "\xa0")
                pages.append(f"**{cog_name}**\
                             \n\n{', '.join(command_names)}\
                             \n\n> Use `{self.context.clean_prefix} help <command>` for more info on a command.")
        
        await self.get_destination().send(content=pages[0], view=PaginationView(pages=pages))


    async def send_command_help(self, command: commands.Command):
        '''
        Sends help for a specific command.
        '''
        
        description_text = command.description or "No description available."
        command_signature = self.get_command_signature(command)
        
        help_embed = discord.Embed(title=f"{command_signature}", description=description_text)
        
        for params_name, params in command.clean_params.items():
            help_embed.add_field(name=params_name.capitalize(), value=params.description, inline=False)
        
        aliases = ", ".join(command.aliases) if command.aliases else "None"
        help_embed.add_field(name="Aliases", value=aliases, inline=False)
        help_embed.set_footer(text='Powered by Vampire')
        await self.get_destination().send(embed=help_embed)

    async def send_cog_help(self, cog: Cog) -> None:
        '''
        Sends help for a specific cog.
        '''
        pages = []
        filtered_commands = await self.filter_commands(cog.get_commands(), sort=True)
        command_names = [command.name for command in filtered_commands]
        if command_names:
            cog_name = cog.qualified_name.replace(" ", "\xa0")
            for command in filtered_commands:
                line = f'```{cog_name}```'
                description_text = command.description or "No description available."
                command_signature = self.get_command_signature(command)
                line += f'```# {command_signature}\n\n{description_text}\n'
                
                for params_name, params in command.clean_params.items():
                    line += f"\n{params_name.capitalize()}: {params.description}"
                
                aliases = ", ".join(command.aliases) if command.aliases else "None"

                line += f'\nAliases\n{aliases}```'
                line += f'> Use `{self.context.clean_prefix} help <command>` for more info on a command.'
                
                pages.append(line)


        await self.get_destination().send(content=pages[0], view=PaginationView(pages=pages))

