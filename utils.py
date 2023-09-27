from datetime import datetime
import discord
from discord.ext.commands import Context
from discord import Embed

def embed_message(title:str, ctx: Context, color: discord.Color) -> Embed:

  description = f"Server: {ctx.guild.name} (ID: {ctx.guild.id})\nAuthor: {ctx.author.mention} (ID: {ctx.author.id})\nLocation: {ctx.message.jump_url}"

  return Embed(
    title=title,
    description=description,
    timestamp=datetime.now(),
    color=color
  )