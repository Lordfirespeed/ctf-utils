from random import SystemRandom


_inst = SystemRandom()
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
binomialvariate = _inst.binomialvariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getrandbits = _inst.getrandbits
randbytes = _inst.randbytes


# copied from python stdlib `secrets.py`
def randbelow(exclusive_upper_bound):
    """Return a random int in the interval [0, n)."""
    if exclusive_upper_bound <= 0:
        raise ValueError("Upper bound must be positive.")
    return _inst._randbelow(exclusive_upper_bound)


# derived from https://docs.python.org/3/library/random.html#random.binomialvariate
def coin_flip(p=0.5) -> bool:
    return random() < p


__all__ = (
    "betavariate",
    "binomialvariate",
    "choice",
    "choices",
    "coin_flip",
    "expovariate",
    "gammavariate",
    "gauss",
    "getrandbits",
    "lognormvariate",
    "normalvariate",
    "paretovariate",
    "randbytes",
    "randint",
    "random",
    "randbelow",
    "randrange",
    "sample",
    "shuffle",
    "triangular",
    "uniform",
    "vonmisesvariate",
    "weibullvariate",
)
