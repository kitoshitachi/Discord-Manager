import re
import random

def random_stat(n, total):
    """Return a randomly chosen list of n nonnegative integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total + n), n - 1))
    return [a - b - 1 for a, b in zip(dividers + [total + n], [0] + dividers)]



def deEmojify(text:str):
    regrex_pattern = re.compile(pattern = "["u"\u0000-\uFFFF""]+", flags = re.UNICODE).finditer
    result = " ".join(match.group() for match in regrex_pattern(text))
    
    return re.sub(r'[❄✡♀]+', '', result)

def clean_name(name:str):
    name = re.sub(r"[._ ]+", ' ', name) # remove dot, whitespaces and underline
    return name.capitalize()
