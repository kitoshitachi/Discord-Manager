

# Standard Library
from typing import List, Optional

# Third Party Library
import discord
from discord.ui import Button, View, button
from discord import ButtonStyle, Embed

# Local Application/Library Specific
from settings import CONFIG
class PaginationView(View):
    def __init__(self, pages:List[Embed], command_user_id:int):
        super().__init__()
        self.page = 0
        self.pages = pages
        self.command_user_id = command_user_id
        self.config = CONFIG

    def is_user_authorization(self, interaction: discord.Interaction):
        return interaction.user.id == self.command_user_id

    @button(label="<", style=ButtonStyle.green, custom_id="prev")
    async def prev_button(self, interaction: discord.Interaction, button: Button):
        if not self.is_user_authorization(interaction):
            return await interaction.response.send_message(f"{self.config['ERROR_EMOJI']}| You can't use this button", ephemeral=True)

        if self.page > 0:
            self.page -= 1
        else:
            self.page = len(self.pages) - 1
            
        await interaction.response.edit_message(embed=self.pages[self.page])

    @button(label=">", style=ButtonStyle.green, custom_id="next")
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if not self.is_user_authorization(interaction):
            return await interaction.response.send_message(f"{self.config['ERROR_EMOJI']}| You can't use this button", ephemeral=True)

        if self.page < len(self.pages) - 1:
            self.page += 1
        else:
            self.page = 0
        await interaction.response.edit_message(embed=self.pages[self.page])

