from typing import Callable

from extras.random_extras.sysrandom import randrange

from .params import DSAParams
from .keys import DSAPrivateKey, DSAPublicKey


type HashFunction = Callable[[int, DSAParams], int]  # type of function H: {0, 1}* -> Z_q


class DSAScheme:
    def __init__(self, hash_function: HashFunction) -> None:
        self.hash_function = hash_function

    def signature_for(self, message: int, key: DSAPrivateKey) -> (int, int):
        def F(group_element: int) -> int:
            nonlocal key
            return group_element % key.params.q

        def H(group_element: int) -> int:
            nonlocal self, key
            return self.hash_function(group_element, key.params)

        k = randrange(1, key.params.q)
        r = F(pow(key.params.g, k, mod=key.params.p))
        if r == 0:
            return self.signature_for(message, key)
        s = pow(k, -1, mod=key.params.q) * ((H(message) + key.private * r) % key.params.q) % key.params.q
        if s == 0:
            return self.signature_for(message, key)
        return r, s

    def verify_signature(self, message: int, signature: (int, int), key: DSAPublicKey) -> int:
        def F(group_element: int) -> int:
            nonlocal key
            return group_element % key.params.q

        def H(group_element: int) -> int:
            nonlocal self, key
            return self.hash_function(group_element, key.params)

        r, s = signature

        generator_exponent = H(message) * pow(s, -1, mod=key.params.q) % key.params.q
        public_exponent = r * pow(s, -1, mod=key.params.q) % key.params.q

        generator_component = pow(key.params.g, generator_exponent, mod=key.params.p)
        public_component = pow(key.public, public_exponent, mod=key.params.p)

        round_trip_r = F(generator_component * public_component % key.params.p)
        return round_trip_r == r
