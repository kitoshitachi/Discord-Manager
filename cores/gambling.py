from dataclasses import dataclass
from random import choice
from typing import Literal
from settings import CONFIG
@dataclass(repr=False, eq=False)
class Slot:
    items = {
        # ':smile:'  : 1, 
        # ':ghost:'  : 2, 
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

    staticmethod
    def help() -> str:
        available_option = "\n".join(f"{key} x{value}" for key, value in Slot.items.items())

        description = "Slot Game\nWith three identical items you will multiply the bet, \
                \notherwise you will lose the bet if it is different."
        return description + "\nList reward:\n" + available_option

class CoinFlip:

    Options = (CONFIG['HEAD_COIN_EMOJI'], CONFIG['TAIL_COIN_EMOJI'])

    @staticmethod
    def play() -> Literal['head','tail']:
        '''
        return face of coin
        '''
        return choice(CoinFlip.Options)
    
    @staticmethod
    def help() -> str:
        available_option = " | ".join(face for face in CoinFlip.Options)
        description = f"{CONFIG['COIN_SPINS_EMOJI']} Coin Flip Game. Choose the face to bet, u will win if you guess right"
        return description + "\nOption is " + available_option
