""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
from discord import app_commands
from discord.ext.commands import Context, Cog, hybrid_command

# Here we name the cog and create a new class for the cog.
class Template(Cog, name="Template"):

  def __init__(self, bot):
    self.bot = bot

  @hybrid_command(
    test="test",
    description="test do nothing",
  )
  @app_commands.describe(template="template")
  async def test(self, ctx: Context, *, test: str) -> None:
    pass
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
  async def setup(bot):
    await bot.add_cog(Template(bot))
