# Standard library imports
from __future__ import annotations
from math import ceil
from random import randint, random, choice, uniform
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

# Third-party imports
from discord.ext.commands import Converter, Context, BadArgument

# Local application/library specific imports
from cores.utils import random_stat
from settings import CONFIG


@dataclass_json
@dataclass(slots=True)
class Stat(Converter):
    HP: float = field(default=0.0, init=True)
    MP: float = field(default=0.0, init=True)
    STR: float = field(default=0.0, init=True)
    AGI: float = field(default=0.0, init=True)
    PR: float = field(default=0.0, init=True)
    CR: float = field(default=0.0, init=True)

    async def convert(self, ctx: Context, argument: str) -> Stat:
        argument = argument.upper()
        if argument in self.__annotations__.keys():
            return argument
        else:
            raise BadArgument(
                "Invalid display_stat name! Options are: HP, MP, STR, AGI, PR, CR.")

    def __add__(self, other):
        if isinstance(other, Stat):
            return Stat(HP=self.HP + other.HP,
                        MP=self.MP + other.MP,
                        STR=self.STR + other.STR,
                        AGI=self.AGI + other.AGI,
                        PR=self.PR + other.PR,
                        CR=self.CR + other.CR)
        else:
            raise TypeError(
                "unsupported operand type(s) for +: 'Stat' and 'str'")

    def __repr__(self) -> str:
        max_len = len(str(self.HP)) + 1
        return f"\
            \nHP : {self.HP:0>{max_len}} MP : {self.MP:0>{max_len}}\n\
            \nSTR: {self.STR:0>{max_len}} AGI: {self.AGI:0>{max_len}}\n\
            \nPR : {self.PR:0>{max_len}} CR : {self.CR:0>{max_len}}\n"


@dataclass_json
@dataclass(slots=True)
class Infor():
    level: int = field(default=1, init=True)
    xp: int = field(default=0, init=True)
    spirit: int = field(default=10, init=True)
    cash: int = field(default=10000, init=True)
    _total_xp: int = field(default=None, init=False, repr=False)

    @property
    def total_xp(self):
        if self._total_xp is None:
            self._total_xp = ceil(self.level / CONFIG['X'])**CONFIG['Y']
        return self._total_xp

    def __repr__(self) -> str:
        return f"\nLevel: {self.level} ({self.xp}/{self.total_xp} XP)\
            \nCash: {self.cash:,}\
            \nSpirit: {self.spirit} XP"

    def level_up(self):
        while self.xp >= self.total_xp:
            self.level += 1
            self.spirit += CONFIG['SPIRIT_PER_LEVEL']
            self.xp -= self.total_xp
            self._total_xp = None  # Reset _total_xp so it gets recalculated

    def add_cash(self, amount: int):
        if amount < 0:
            raise BadArgument("Amount must be a positive integer")
        self.cash += amount

    def decrease_spirit(self, amount: int):
        if amount < 0:
            raise BadArgument("Amount must be a positive integer")
        self.spirit -= amount
        if self.spirit < 0:
            self.spirit = 0

    def remaining_xp(self):
        return self.total_xp - self.xp

    def add_xp(self, amount: int):
        if amount < 0:
            raise BadArgument("Amount must be a positive integer")
        self.xp += amount
        self.level_up()

    def add_spirit(self, amount: int):
        if amount < 0:
            raise BadArgument("Amount must be a positive integer")
        self.spirit += amount

    def decrease_cash(self, amount: int):
        if amount < 0:
            raise BadArgument("Amount must be a positive integer")
        self.cash -= amount
        if self.cash < 0:
            self.cash = 0

    def update(self, xp: int = 0, cash: int = 0):
        '''
        return True if level up
        '''
        if xp < 0 or cash < 0:
            raise BadArgument("Values must be positive integers")

        old_level = self.level
        self.xp += xp
        self.cash += cash
        self.level_up()
        return self.level > old_level

    def reset_spirit(self):
        self.spirit = self.level * CONFIG['SPIRIT_PER_LEVEL']

@dataclass(frozen=True, eq=False, init=False)
class FantasyWorld:

    @staticmethod
    def gift():
        '''
        return xp, cash, stat_increase
        '''
        xp = randint(CONFIG['MIN_EXP'], CONFIG['MAX_EXP'])
        cash = randint(CONFIG['MIN_COINS'], CONFIG['MAX_COINS'])

        stat_name = choice(list(Stat.__annotations__))
        stat_increase = CONFIG['BIG_STAT_INCREASE'] if 1 - random() < CONFIG['STAT_PROBABILITY'] else CONFIG['SMALL_STAT_INCREASE']
        return xp, cash, stat_name, stat_increase


@dataclass_json
@dataclass(slots=True)
class BaseCharacter:
    base_stat: Stat = field(default_factory= lambda: Stat(*random_stat(6, 6)))
    bonus_stat: Stat = field(default_factory=Stat)
    infor: Infor = field(default_factory=Infor)


    @property
    def total_stat(self) -> Stat:
        '''
        Calculate and return the character's total stats based on base and bonus stats.
        '''
        return self.base_stat + self.bonus_stat

    @property
    def display_stat(self) -> Stat:
        '''
        Display the character's stats based on base and bonus stats.
        '''
        _stat = self.total_stat

        return Stat(int(_stat.HP * 20 + 500), int(_stat.MP * 20 + 250),
                    int(_stat.STR * 5 + 100), int(_stat.AGI * 4 + 100),
                    int(_stat.PR * 2 + 20), int(_stat.CR))

    def __repr__(self) -> str:
        return f"═══════════ Character Information ═══════════\n\
                {self.infor.__repr__()}\n\
                {self.display_stat.__repr__()}\
                \n═════════════════════════════════════════════"

class Character(BaseCharacter):

    def upgrade(self, display_stat: str, spirit: int):
        '''
        Use spirit to upgrade a bonus stat of the character.
        '''
        if spirit == "all":
            spirit = self.infor.spirit

        if spirit > self.infor.spirit:
            raise BadArgument("You don't have enough spirits!")

        setattr(self.bonus_stat, display_stat.upper(),
                spirit + getattr(self.bonus_stat, display_stat.upper()))
        self.infor.decrease_spirit(spirit)
        return f"You have upgraded {spirit} {display_stat}."

    def train(self, limited_xp: int, status: int) -> tuple[int, int, str, bool]:
        '''
        Train the character with limited xp and status.
        return xp, cash, stat_name, stat_increase, is_lvl_up
        '''
        xp, cash, stat_name, stat_increase = FantasyWorld.gift()

        if limited_xp <= xp:
            xp = limited_xp

        if status <= 0:
            status = 0
            stat_increase = 0
        else:
            setattr(self.base_stat, stat_name.upper(),
                    getattr(self.base_stat, stat_name.upper()) + stat_increase)

        is_lvl_up = self.infor.update(xp, cash)

        return xp, cash, stat_name, stat_increase, is_lvl_up

    def attack(self):
        '''
        Calculate and return the total damage dealt by the character.
        If the character lands a critical hit, the damage is multiplied by 2.
        '''
        damage = self.display_stat.STR
        if random() < self.display_stat.CR / 100:  # Critical hit chance
            damage *= 2  # Critical hit multiplier

        return damage

    def dodge(self):
        if random() < (self.display_stat.AGI / (self.display_stat.AGI + 100))**3:
            return True

        return False

    def parry(self):
        total = self.display_stat.AGI + self.display_stat.PR
        max_reduce = (total / (total + 100))**2

        return uniform(0.0, max_reduce)

    def reflect_damage(self, damage):
        '''
        Calculate and return the reflected damage based on the character's HP and DEF.
        '''
        reflect_percentage = (self.display_stat.HP + self.display_stat.PR) / 1000  # Adjust this formula as needed
        return damage * reflect_percentage

    def deal_damage(self, other: Character):
        '''
        Calculate and return the total damage dealt by the character to another character.
        Also, calculate the reflected damage and subtract it from the character's HP.
        '''
        if other.dodge():
            return 0

        damage = self.attack()
        reduction = other.parry()
        final_damage = damage * (1 - reduction)

        reflected_damage = other.reflect_damage(final_damage)
        self.display_stat.HP -= reflected_damage  # Subtract reflected damage from attacker's HP

        return final_damage

    def total_damage_received(self, attacker: Character):
        '''
        Calculate and return the total damage received by the character.
        '''
        return attacker.deal_damage(self)
