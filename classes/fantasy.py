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
        stat = 0.001 if random() < 0.9 else 0.002
        luck_stat = 0 if random() < (1 - 0.0001) else 1
        return xp, cash, stat, luck_stat
    
    