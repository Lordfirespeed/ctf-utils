from dataclasses import dataclass
from typing import Sequence

from sympy import Poly, Symbol, poly
from sympy.abc import x

from extras.random_extras.sysrandom import randrange, sample


@dataclass
class Share:
    id: int
    alpha: int
    y: int


def compute_shares_of_secret(secret: Poly, modulus: int, party_count: int) -> list[Share]:
    assert secret.atoms(Symbol) == {x}, "Secret should be a univariate polynomial in `x`"
    threshold_count = secret.degree(x) + 1
    assert threshold_count <= party_count, "Party count should be greater than the degree of the secret (in `x`)"

    # randomly sample from the field until we have enough 'alpha' values
    assert modulus > party_count
    alphas: set[int] = set()
    while len(alphas) < party_count:
        alphas.add(randrange(1, modulus))

    # compute the corresponding 'y' values for each 'alpha' value
    shares: list[Share] = []
    alphas_iter = iter(alphas)
    for party_member_index in range(party_count):
        alpha = next(alphas_iter)
        y = secret(alpha) % modulus
        shares.append(Share(
            id=party_member_index,
            alpha=alpha,
            y=y,
        ))

    return shares


def reconstruct_secret(shares: Sequence[Share], modulus: int) -> Poly:
    accumulator = poly(0, x, domain="ZZ")

    def delta_k(index_i: int) -> Poly:
        nonlocal shares, modulus
        delta_accumulator = poly(1, x, domain="ZZ")
        for index_j in range(len(shares)):
            if index_i == index_j:
                continue
            delta_accumulator *= (x - shares[index_j].alpha)
            delta_accumulator = delta_accumulator.trunc(modulus)
            divisor = pow(shares[index_i].alpha - shares[index_j].alpha, -1, mod=modulus)
            delta_accumulator *= divisor
            delta_accumulator = delta_accumulator.trunc(modulus)
        return delta_accumulator

    for index_i in range(len(shares)):
        y = shares[index_i].y
        y *= delta_k(index_i)
        accumulator += y
        accumulator = accumulator.trunc(modulus)
    return accumulator


q = 65537
secret = poly(58264 + 4221 * x + 8563 * pow(x, 2) + 51868 * pow(x, 3), x, domain="ZZ")
threshold = secret.degree(x) + 1
shares = compute_shares_of_secret(secret, q, 16)


def attempt_reconstruction_with(n_conspirators: int) -> None:
    subset = sample(shares, n_conspirators)
    reconstruction = reconstruct_secret(subset, q)
    print(f"with {n_conspirators:02} conspirators:")
    print(f"{'':4}{secret.as_expr() = !s}")
    print(f"{'':4}{reconstruction.as_expr() = }")
    print(f"{'':4}{reconstruction == secret.trunc(q) = }")


def main():
    for conspirator_count in (2, 3, 4, 5, 9, 16):
        attempt_reconstruction_with(conspirator_count)


__all__ = ("Share", "compute_shares_of_secret", "reconstruct_secret",)


if __name__ == "__main__":
    main()
