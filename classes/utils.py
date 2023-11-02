import random
from discord import Client
from discord.ext.commands import Context
from classes.database import Database

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def random_stat(n, total):
    """Return a randomly chosen list of n nonnegative integers summing to total.
    Each such list is equally likely to occur."""

    return [x - 1 for x in constrained_sum_sample_pos(n, total + n)]

async def create_member(ctx:Context, bot: Client, database:Database) -> None:
    """
    create new member data
    """
    message = await ctx.channel.send('Agree to activate the system?')
    await message.add_reaction('✅')
    await message.add_reaction('❎')
    valid_reactions = ['✅', '❎']
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reactions

    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)

    if str(reaction.emoji) == valid_reactions[0]:
        result = database.init_member(ctx.author.id) 
        if result == True:
            await message.edit(content="Success!")
        else:
            await message.edit(content="Cancelled!")
    else:
        await message.edit(content="Cancelled!")