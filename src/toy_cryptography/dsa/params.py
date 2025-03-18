from dataclasses import dataclass

from extras.math_extras import miller_rabin_primality_test as probable_prime
from extras.math_extras.related_prime import find_related_prime
from extras.random_extras import prime_randint_of_digit_length
from extras.random_extras.sysrandom import randrange


@dataclass
class DSAParams:
    p: int
    q: int
    g: int

    def __post_init__(self):
        assert probable_prime(self.p), \
            "p should be (probably) prime"
        assert probable_prime(self.q), \
            "q should be (probably) prime"
        multiplier, remainder = divmod(self.p - 1, self.q)
        assert remainder == 0, \
            "p should be of the form kq+1 for some integer k"
        assert pow(self.g, self.q, mod=self.p), \
            "g should generate a multiplicative (mod p) group of prime order q"


def determine_params(prime_p: int, prime_q: int, subgroup_generator_index: int = None) -> DSAParams:
    multiplier, _ = divmod(prime_p - 1, prime_q)

    def generates_group(group_element: int) -> bool:
        """
        Order of multiplicative group mod p is `kq`.

        By Lagrange's little thm., subgroup orders must divide the group.
        So if element `a` generates a (strict) subgroup, either:
          - its order is `q`, in which case `a^q = 1`
          - its order is a factor of `k`, in which case `a^k = 1`

        Hence, check `a` generates the whole group by verifying `a^k != 1` and `a^q != 1`.
        """
        if pow(group_element, multiplier, mod=prime_p) == 1:
            return False
        if pow(group_element, prime_q, mod=prime_p) == 1:
            return False
        return True

    group_generators = filter(generates_group, range(2, prime_p))
    group_generator = next(group_generators)

    # choose some integer l from (0, q)
    if subgroup_generator_index is None:
        subgroup_generator_index = randrange(1, prime_q)
    else:
        subgroup_generator_index %= prime_q
        assert subgroup_generator_index > 0
    # set g = pow(a, l * k, mod=p) = pow(a, (l * k) % (q * k), mod=p)
    subgroup_generator_exponent = (subgroup_generator_index * multiplier) % (prime_p - 1)
    subgroup_generator = pow(group_generator, subgroup_generator_exponent, mod=prime_p)
    # g generates a group of prime order `q` (hooray!)

    return DSAParams(
        q=prime_q,
        p=prime_p,
        g=subgroup_generator,
    )


def gen_params(prime_digit_length: int = 68) -> DSAParams:
    # choose primes p, q such that p = kq+1 for some k
    prime_q = prime_randint_of_digit_length(prime_digit_length)
    prime_p = find_related_prime(prime_q, 500)
    return determine_params(prime_p, prime_q)


__all__ = ("DSAParams", "gen_params",)
