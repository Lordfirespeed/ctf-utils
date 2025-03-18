from dataclasses import dataclass, field
from math import gcd

from extras.math_extras import miller_rabin_primality_test as probable_prime
from extras.random_extras import prime_randint_of_digit_length, randint_coprime_to


@dataclass
class RSAPublicKey:
    modulus: int
    public_exponent: int


@dataclass
class RSAPrivateKey:
    # stored values absolutely necessary for any implementation
    modulus: int  # 'n = pq'
    public_exponent: int  # 'e'
    private_exponent: int  # 'd = e^{-1} mod phi(n)'

    # stored values only used for more efficient implementation & integrity checks
    # see https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Using_the_Chinese_remainder_algorithm
    prime1: int = field(repr=False)  # 'p'
    prime2: int = field(repr=False)  # 'q'
    private_exponent1: int = field(repr=False)  # 'd_p = d mod (p-1)'
    private_exponent2: int = field(repr=False)  # 'd_q = d mod (q-1)'
    coefficient: int = field(repr=False)  # 'q_{inv} = q^{-1} mod p`

    @property
    def group_order(self) -> int:
        return (self.prime1 - 1) * (self.prime2 - 1)

    def __post_init__(self):
        assert probable_prime(self.prime1), \
            "prime1 should be (probably) prime"
        assert probable_prime(self.prime2), \
            "prime2 should be (probably) prime"
        assert self.modulus == self.prime1 * self.prime2, \
            "modulus should be product of prime1 and prime2"
        assert gcd(self.public_exponent, self.group_order) == 1, \
            "public_exponent should be co-prime to phi(modulus)"
        assert (self.public_exponent * self.private_exponent) % self.group_order == 1, \
            "private_exponent should be public_exponent's mul. inverse mod phi(modulus)"
        assert self.private_exponent1 == self.private_exponent % (self.prime1 - 1), \
            "private_exponent1 should be private_exponent mod (prime1 -1 )"
        assert self.private_exponent2 == self.private_exponent % (self.prime2 - 1), \
            "private_exponent2 should be private_exponent mod (prime2 - 1)"
        assert (self.prime2 * self.coefficient) % self.prime1 == 1, \
            "coefficient should be prime2's mul. inverse mod prime1"

    def extract_public_key(self) -> RSAPublicKey:
        return RSAPublicKey(
            modulus=self.modulus,
            public_exponent=self.public_exponent,
        )


def determine_private_key(
    prime1: int,  # p
    prime2: int,  # q
    public_exponent: int,  # e
) -> RSAPrivateKey:
    modulus = prime1 * prime2
    group_order = (prime1 - 1) * (prime2 - 1)  # phi(modulus)
    private_exponent = pow(public_exponent, -1, mod=group_order)

    private_exponent1 = private_exponent % (prime1 - 1)
    private_exponent2 = private_exponent % (prime2 - 1)
    coefficient = pow(prime2, -1, mod=prime1)

    return RSAPrivateKey(
        modulus=modulus,
        public_exponent=public_exponent,
        private_exponent=private_exponent,

        prime1=prime1,
        prime2=prime2,
        private_exponent1=private_exponent1,
        private_exponent2=private_exponent2,
        coefficient=coefficient,
    )


def gen_private_key(prime_digit_length: int = 12) -> RSAPrivateKey:
    prime1 = prime_randint_of_digit_length(prime_digit_length)
    prime2 = prime_randint_of_digit_length(prime_digit_length)
    group_order = (prime1 - 1) * (prime2 - 1)
    public_exponent = randint_coprime_to(group_order)

    return determine_private_key(prime1, prime2, public_exponent)


__all__ = ("RSAPublicKey", "RSAPrivateKey", "determine_private_key", "gen_private_key",)
