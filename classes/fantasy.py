from __future__ import annotations
from math import ceil
from typing import Literal
import yaml
from random import randint, random, choice, uniform
from dataclasses import dataclass
from classes.utils import random_stat

with open('config.yml','r') as f:
    config = yaml.safe_load(f)
@dataclass(eq=False)
class Stat:
    HP: float = 0
    MP: float = 0
    STR: float = 0
    AGI: float = 0
    PR: float = 0
    CR: float = 0

    def __setattr__(self, __name: str, __value: float) -> None:
        if not isinstance(self, Stat):
            raise NotImplemented
        if __name not in Stat.__annotations__:
            raise AttributeError
        
        super().__setattr__(__name, round(__value,3))


    def __add__(self, other):
        if not isinstance(other, Stat):
            raise NotImplemented
        return Stat(
            self.HP + other.HP,
            self.MP + other.MP,
            self.STR + other.STR,
            self.AGI + other.AGI,
            self.PR + other.PR,
            self.CR + other.CR,
        )

    def __repr__(self) -> str:
        max_len = len(str(self.HP)) + 1
        # return f"\nHP: {self.HP:0>{max_len}}\tSTR: {self.STR:0>{max_len}}\tPR: {self.PR:0>{max_len}} \
        #     \nMP: {self.MP:0>{max_len}}\tAGI: {self.AGI:0>{max_len}}\tCR: {self.CR:0>{max_len}}\n"
    
        return f"\
            \n🩸 {self.HP:0>{max_len}} 💧 {self.MP:0>{max_len}}\n\
            \n💪 {self.STR:0>{max_len}} 🦵 {self.AGI:0>{max_len}}\n\
            \n🛡️ {self.PR:0>{max_len}} 💥 {self.CR:0>{max_len}}\n"
    # @staticmethod
    


@dataclass(eq=False)
class Infor:
    level: int = 1
    xp: int = 0
    spirit: int = 10
    cash: int = 10000
    
    @property
    def total_xp(self):
        return ceil( self.level / config['X'] ) ** config['Y']

    def __setattr__(self, __name: str, __value: int) -> None:
        if isinstance(self, Infor) and __name in self.__annotations__:
            super().__setattr__(__name, __value)
        else:
            raise AttributeError(f"{__name} Not Found !")

    def __repr__(self) -> str:
        return f"\nLevel: {self.level} ({self.xp}/{self.total_xp} XP)\
            \nCash: {self.cash:,}\
            \nSpirit: {self.spirit} XP"



@dataclass(frozen=True, eq=False, init=False)
class FantasyWorld:

    @staticmethod
    def gift():
        '''
        return xp, cash, stat
        
        '''
        xp = randint(config['MIN_EXP'], config['MAX_EXP'])
        
        cash = randint(config['MIN_COINS'], config['MAX_COINS'])

        stat_name = list(Stat.__annotations__)
        
        return xp, cash, {
            choice(stat_name[:4]): 0.001 if random() < 0.99 else 0.002,
            choice(stat_name[4:]): 1 if random() < 0.005 else 0
        }

@dataclass(eq=False)
class Character:
    base_stat: Stat = Stat(*random_stat(6,6))
    bonus_stat: Stat = Stat()
    infor: Infor = Infor()

    @property
    def stat(self):
        '''
        return hp, mp, str, agi, pr, cr
        '''
        _stat = self.base_stat + self.bonus_stat
        
        return Stat(
            int(_stat.HP * 20 + 500),
            int(_stat.MP * 20 + 250),
            int(_stat.STR * 5 + 100),
            int(_stat.AGI * 4 + 100),
            int(_stat.PR * 2 + 20),
            int(_stat.CR)
        )
    
    def __add_stat__(self, data:dict, where:Literal['base_stat', 'bonus_stat'] = 'base_stat'):
        stat = getattr(self, where)
        for name, value in data.items():
            setattr(stat, name, value + getattr(stat, name))
             

    def upgrade(self, stat:str, spirit:int):

        if spirit > self.infor.spirit:
            return "You don't have enought spirits !"
        
        self.__add_stat__({stat.upper():spirit}, 'bonus_stat')
        self.infor.spirit -= spirit
        return f"You have upgraded {spirit} {stat}."
        
        

    def __repr__(self) -> str:
        return f"═══════════ Character Information ═══════════\n\
                {self.infor.__repr__()}\n\
                {self.stat.__repr__()}\
                \n═════════════════════════════════════════════"

    def __is_level_up(self) -> bool:
        total_xp = ceil( self.infor.level / config['X'] ) ** config['Y']
        if self.infor.xp >= total_xp:
            self.infor.level += 1
            self.infor.xp -= total_xp

            self.infor.spirit += config['STAT_PER_LEVEL']
            return True
        
        return False
        
    def train(self, limited_xp:int, status:int):
        '''
        return xp, cash, stat, msg
        '''
        xp, cash, stat = FantasyWorld.gift()
        

        if limited_xp <= xp:
            xp = limited_xp


        if status <= 0:
            status = 0
            cash = 0
            stat = None  
        else:
            self.__add_stat__(stat)        

        self.infor.xp += xp   
        self.infor.cash += cash

        msg = None    
        if self.__is_level_up():
            msg = f"Leveled up! Ur level is {self.infor.level}."
        
        return xp, cash, stat, msg

    def attack(self):
        return self.stat.STR * (2 if random() < self.stat.CR / 100 else 1)
    
    def dodge(self):
        if random() < (self.stat.AGI/(self.stat.AGI + 100)) ** 3:
            return True 
            
        return False
    
    def parry(self):
        total = self.stat.AGI + self.stat.PR
        max_reduce = (total/(total + 100)) ** 2
        
        return uniform(0.0,max_reduce)