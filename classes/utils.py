from discord import Client
from discord.ext import commands
from discord.ext.commands import Context
from classes.database import Database

async def create_member(bot: Client, database:Database , context:Context, _id:int) -> None:
    """
    create new member data
    """
    message = await context.channel.send('Agree to activate the system?')
    await message.add_reaction('✅')
    await message.add_reaction('❎')
    valid_reactions = ['✅', '❎']
    def check(reaction, user):
        return user == context.author and str(reaction.emoji) in valid_reactions

    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

    if str(reaction.emoji) == valid_reactions[0]:
        if database.init_member(_id) == False:
            raise commands.MissingRequiredArgument
        await message.edit(content="Success!")
    else:
        await message.edit(content="Cancelled!")