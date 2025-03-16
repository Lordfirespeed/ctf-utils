from extras.math_extras import extended_euclidian_algorithm
from extras.random_extras.sysrandom import randbelow


def randint_coprime_to(value: int) -> int:
    """Return a random integer (non-trivially) co-prime to `value`."""
    if value <= 2:
        # reject negative values
        # 0's unique positive co-prime value is 1, but 1 is trivial, so reject
        # similar argument for 1, 2
        raise ValueError

    def make_coprime(trial_value: int) -> int:
        """Return an integer co-prime to `value` which may be trivial, depending on `trial_value`"""
        while True:
            if trial_value == 1:
                break

            gcd = extended_euclidian_algorithm(trial_value, value).gcd
            if gcd == 1:
                break

            trial_value //= gcd
        return trial_value

    while True:
        candidate = randbelow(value)
        if candidate == 0:
            continue
        candidate = make_coprime(candidate)
        if candidate != 1:
            break

    return candidate


__all__ = ("randint_coprime_to",)
