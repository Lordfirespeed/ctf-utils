from dataclasses import dataclass

from extras.random_extras.sysrandom import randrange

from .params import DSAParams


@dataclass
class DSAPublicKey:
    public: int
    params: DSAParams


@dataclass
class DSAPrivateKey:
    private: int
    public: int
    params: DSAParams

    def __post_init__(self):
        assert 1 < self.private < self.params.q, \
            "private key should live in the interval (1, q)"
        assert 1 < self.public < self.params.p, \
            "public key should live in the interval (1, p)"
        assert pow(self.params.g, self.private, mod=self.params.p) == self.public, \
            "public group element should be g^private mod p"

    def extract_public_key(self) -> DSAPublicKey:
        return DSAPublicKey(
            public=self.public,
            params=self.params,
        )


def determine_private_key(params: DSAParams, private: int) -> DSAPrivateKey:
    public = pow(params.g, private, mod=params.p)
    return DSAPrivateKey(
        private,
        public,
        params,
    )


def gen_private_key(params: DSAParams) -> DSAPrivateKey:
    private = randrange(2, params.q)
    return determine_private_key(params, private)


__all__ = ("DSAPublicKey", "DSAPrivateKey", "determine_private_key", "gen_private_key",)
