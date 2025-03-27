from extras.binary_extras.bit_set import BitSet


def sieve_primes_less_than(bound: int) -> list[int]:
    primes = []
    sieve = BitSet(bound)
    sieve[0] = True
    prime = 1

    while True:
        prime = sieve.next_clear_bit_index(prime - 1) + 1
        if prime >= bound:
            break
        primes.append(prime)

        cursor = prime - 1
        while cursor < bound:
            sieve[cursor] = True
            cursor += prime

    return primes


__all__ = ("sieve_primes_less_than",)
