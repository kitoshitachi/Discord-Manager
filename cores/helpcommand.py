from typing import List, Mapping, Optional
import discord

from discord.ext import commands
from discord.ext.commands import Cog, Command
from cores.view import PaginationView

from settings import CONFIG

class CustomHelpCommand(commands.HelpCommand):
    '''
    A custom help command for the Discord bot.

    '''
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Shows help about the bot, a command, or a category',
            'cooldown': commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.user)
        })
        self.config = CONFIG

    def get_command_signature(self, command: Command):
        return f"{self.context.clean_prefix} {command.name} {command.signature}"

    async def send_bot_help(self, mapping:Mapping[Optional[Cog], List[Command]]):
        '''
        Sends help for the bot.
        '''

        pages = []

        for cog, commands in mapping.items():
            if cog is None:
                continue
            filtered_commands = await self.filter_commands(commands, sort=True)
            command_names = [command.name for command in filtered_commands]
            if command_names:
                cog_name, cog_description = cog.description.split('\n')

                help_embed = discord.Embed(
                    title=cog_name,
                    description=cog_description,
                    color=self.config['BLACK']
                )

                help_embed.add_field(name="List command", value=", ".join(command_names), inline=False)
                help_embed.add_field(name='', value=f"`{self.config['NOTICE_EMOJI']} | {self.context.clean_prefix} help <command | group>`", inline=False)
                
                help_embed.set_footer(text='Powered by Vampire')

                pages.append(help_embed)

        await self.get_destination().send(embed=pages[0], view=PaginationView(pages, self.context.author.id))

    async def send_cog_help(self, cog: Cog) -> None:
        '''
        Sends help for a specific cog.
        '''
        pages = []
        filtered_commands = await self.filter_commands(cog.get_commands(), sort=True)
        command_names = [command.name for command in filtered_commands]
        if command_names:
            cog_name, cog_description = cog.description.split('\n')
            for command in filtered_commands:

                help_embed = discord.Embed(
                    title=f"{cog_name}",
                    description=cog_description,
                    color=self.config['BLACK']
                )
                
                help_embed.add_field(name='',value='', inline=False)
                

                description_text = command.description or "No description available."
                command_signature = self.get_command_signature(command)
                help_embed.add_field(name=command_signature, value=description_text, inline=False)


                for params_name, params in command.clean_params.items():
                    help_embed.add_field(name=params_name.capitalize(), value=params.description, inline=False)


                aliases = ", ".join(command.aliases) if command.aliases else "None"
                help_embed.add_field(name="", value=f"**Aliases:** {aliases}", inline=False)

                help_embed.add_field(name='', value=f"`{self.config['NOTICE_EMOJI']} | {self.context.clean_prefix} help <command | group>`", inline=False)

                help_embed.set_footer(text='Powered by Vampire')
                
                pages.append(help_embed)


        await self.get_destination().send(embed=pages[0], view=PaginationView(pages, self.context.author.id))


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
