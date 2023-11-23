import random


def random_stat(n, total):
    """Return a randomly chosen list of n nonnegative integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total + n), n - 1))
    return [a - b - 1 for a, b in zip(dividers + [total + n], [0] + dividers)]
