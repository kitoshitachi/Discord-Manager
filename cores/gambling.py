from dataclasses import dataclass
from random import randint, choice

@dataclass(repr=False, eq=False)
class Slot:
    items = {
        'human'  : 1, 
        'ghost'  : 2, 
        'zombie' : 4, 
        'evil'   : 8, 
        'angel'  : 16, 
        'vampire': 32, 
        'hunter' : 100
    }
    # __chance = [20, 20, 20, 20, 10, 5, 5]

    @classmethod
    def slot(cls):
        # return choices(list(cls.__items.keys()), cls.__chance)[0]
        return choice(list(cls.__items.keys()))

    @classmethod
    def play(cls):
        '''
        return multiple bet
        '''
        result = cls.slot(), Slot.slot(), Slot.slot()
        win = len(set(result))
        
        if win == 1:
            return Slot.__items[result[0]], *result
        
        return -1, *result



class CoinFlip:

    @staticmethod
    def play(choice):
        '''
        if win coin flip, return true
        '''
        result = randint(0,1)
        return choice == result
    
