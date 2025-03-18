from extras.random_extras import prime_randint_of_digit_length, randint_of_digit_length

from .primality import miller_rabin_primality_test as probable_prime
from .prime_sieve import sieve_primes_less_than


small_primes = sieve_primes_less_than(72)  # first 20 primes


def find_related_prime(prime_q: int, multiplier_digits_at_least: int = 500) -> int:
    """
    https://crypto.stackexchange.com/a/72677
    :return: a prime integer `p` such that `q` is a factor of `p-1` (`q` divides `p-1`).
    """
    anti_congruences = [(-pow(prime_q, -1, mod=small_prime)) % small_prime for small_prime in small_primes]

    def is_candidate_multiplier(multiplier: int) -> bool:
        nonlocal anti_congruences
        for anti_congruence_index in range(len(small_primes)):
            small_prime = small_primes[anti_congruence_index]
            anti_congruence = anti_congruences[anti_congruence_index]
            if multiplier % small_prime == anti_congruence:
                return False
        return True

    def candidate_multipliers():
        multiplier = randint_of_digit_length(multiplier_digits_at_least)
        while True:
            if not is_candidate_multiplier(multiplier):
                multiplier += 1
                continue

            yield multiplier
            multiplier += 1

    for multiplier in candidate_multipliers():
        prime_p = (prime_q * multiplier) + 1
        if probable_prime(prime_p):
            break
    return prime_p


__all__ = ("find_related_prime",)
