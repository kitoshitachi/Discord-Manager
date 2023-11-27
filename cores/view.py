from typing import List
import discord
from discord.ui import Button, View, button
from discord import ButtonStyle

class PaginationView(View):
    def __init__(self, pages:List[str]):
        super().__init__()
        self.page = 0
        self.pages = pages


    @button(label="<", style=ButtonStyle.green, custom_id="prev")
    async def prev_button(self, interaction: discord.Interaction, button: Button):
        if self.page > 0:
            self.page -= 1
        else:
            self.page = len(self.pages) - 1
        print(self.page)
        await interaction.response.edit_message(content=self.pages[self.page])

    @button(label=">", style=ButtonStyle.green, custom_id="next")
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.page < len(self.pages) - 1:
            self.page += 1
        else:
            self.page = 0
        print(self.page)
        await interaction.response.edit_message(content=self.pages[self.page])