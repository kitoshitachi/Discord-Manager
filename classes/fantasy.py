import yaml
from random import randint, random


class FantasyWorld:
    def __init__(self) -> None:
        with open('config.yml','r') as f:
            self.config = yaml.safe_load(f)

    def get_items(self):
        '''
        return random xp, cash, stat
        
        '''
        xp = randint(self.config['MIN_EXP'], self.config['MAX_EXP'])
        cash = randint(self.config['MIN_COINS'], self.config['MAX_COINS'])
        stat = 0.001 if random() < 0.99 else 0.002
        luck_stat = 0 if random() < (1 - 0.005) else 1
        return xp, cash, stat, luck_stat
    
    def get_stat(self, character = None):
        character['hp'] = int(character['hp'] * 20) + self.config['HP_BASE']
        character['mp'] = int(character['mp'] * 20) + self.config['MP_BASE']
        character['str'] = int(character['str'] * 5) + self.config['STR_BASE']
        character['agi'] = int(character['agi'] * 4) + self.config['AGI_BASE']
        character['def'] = int(character['def'] * 2) + self.config['DEF_BASE']
        character['crit'] = int(character['crit'] * self.config['CRIT_BASE'])
        return character
    
    