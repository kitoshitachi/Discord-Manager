from dataclasses import dataclass
from random import choice
from typing import Literal
from settings import CONFIG
@dataclass(repr=False, eq=False)
class Slot:
    items = {
        ':smile:'  : 1, 
        ':ghost:'  : 2, 
        ':zombie:' : 4, 
        ':imp:'   : 8, 
        ':angel:'  : 16, 
        ':vampire:': 32, 
        CONFIG['CASH_EMOJI'] : 100
    }
    # __chance = [20, 20, 20, 20, 10, 5, 5]

    @staticmethod
    def slot():
        return choice(list(Slot.items.keys()))

    @staticmethod
    def play():
        '''
        return three slot 
        '''   
        return Slot.slot(), Slot.slot(), Slot.slot()



class CoinFlip:

    @staticmethod
    def play() -> Literal['head','tail']:
        '''
        return face of coin
        '''
        return choice('head','tail')
    
