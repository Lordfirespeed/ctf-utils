from string import ascii_uppercase, ascii_lowercase

from bidict import bidict

from toy_cryptography.rsa.keys import *
from toy_cryptography.rsa.scheme import encrypt, decrypt


bob_key = determine_private_key(5, 13, 19)

conversion_order = (
    " ",
    "\n",
    *ascii_uppercase,
    *ascii_lowercase,
    ".",
    ",",
    "?",
    "!",
    ":",
    ";",
    "'",
    "\t",
)
conversion_table = bidict[int, str](enumerate(conversion_order, 2))
# conversion values are [2, 63] because encryptions of 0, 1, 64 are 0, 1, 64 (these values provide no secrecy)


def encrypt_str(message: str, key: RSAPublicKey) -> str:
    numbers = (conversion_table.inverse[character] for character in message)
    encrypted_numbers = (encrypt(number, key) for number in numbers)
    return "".join(conversion_table[number] for number in encrypted_numbers)


def decrypt_str(ciphertext: str, key: RSAPrivateKey) -> str:
    encrypted_numbers = (conversion_table.inverse[character] for character in ciphertext)
    numbers = (decrypt(number, key) for number in encrypted_numbers)
    return "".join(conversion_table[number] for number in numbers)


def main():
    print(f"{bob_key = }")

    alice_message = "Hell"
    alice_ciphertext = encrypt_str(alice_message, bob_key.extract_public_key())
    print(f"{alice_message = }")
    print(f"{alice_ciphertext = }")

    other_ciphertext = ":Uo"
    other_message = decrypt_str(other_ciphertext, bob_key)
    print(f"{other_ciphertext = }")
    print(f"{other_message = }")


if __name__ == "__main__":
    main()
