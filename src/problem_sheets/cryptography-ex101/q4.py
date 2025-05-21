from collections import defaultdict
import itertools
from typing import Generator, Sequence

from bitarray import bitarray, frozenbitarray
from bitarray.util import int2ba

from toy_cryptography.feistel_cipher.scheme import (
    FeistelText,
    encrypt as feistel_encrypt,
    decrypt as feistel_decrypt,
)
from q2 import feistel_function



"""
We use double encryption:
C = e(e(M, K), K')
Where K = (K_1, K_2) and K' = (K'_1, K'_2).
"""
def encrypt(plaintext: FeistelText) -> FeistelText:
    # round keys are unknown
    first_round_keys: Sequence[bitarray]
    second_round_keys: Sequence[bitarray]

    first_step = feistel_encrypt(plaintext, first_round_keys, feistel_function)
    second_step = feistel_encrypt(first_step, second_round_keys, feistel_function)
    return second_step


# a known plaintext/ciphertext pair
plaintext = FeistelText(
    left=frozenbitarray("0111"), right=frozenbitarray("0001")
)
ciphertext = FeistelText(
    left=frozenbitarray("1000"), right=frozenbitarray("0111")
)


def all_round_keys() -> Generator[frozenbitarray]:
    for key_int in range(0b0000, 0b1111 + 1):
        yield frozenbitarray(int2ba(key_int, length=4))


def meet_in_the_middle():
    half_encryption_lookup = defaultdict[FeistelText, set[frozenbitarray]](set)
    first_round_keys: tuple[frozenbitarray, frozenbitarray]
    for first_round_keys in itertools.product(all_round_keys(), repeat=2):
        half_encryption = feistel_encrypt(plaintext, first_round_keys, feistel_function)
        first_key_set = half_encryption_lookup[half_encryption]
        first_key = first_round_keys[0] + first_round_keys[1]
        first_key_set.add(first_key)

    collisions: set[tuple[frozenbitarray, frozenbitarray]] = set()  # set of (K, K')
    second_round_keys: tuple[frozenbitarray, frozenbitarray]
    for second_round_keys in itertools.product(all_round_keys(), repeat=2):
        half_decryption = feistel_decrypt(ciphertext, second_round_keys, feistel_function)
        first_key_set = half_encryption_lookup.get(half_decryption, None)
        if first_key_set is None:
            continue
        second_key = second_round_keys[0] + second_round_keys[1]
        for first_key in first_key_set:
            collisions.add((first_key, second_key))

    return collisions


def main():
    my_collisions = meet_in_the_middle()
    print(f"found {len(my_collisions)} collisions")
    solution_collision = (frozenbitarray("00001000"), frozenbitarray("11111111"))
    print(f"do my collisions contain solution collision: {solution_collision in my_collisions}")
    for k, k_prime in my_collisions:
        print(f"{'':>4}K={k.to01()}, K'={k_prime.to01()}")


if __name__ == "__main__":
    main()
