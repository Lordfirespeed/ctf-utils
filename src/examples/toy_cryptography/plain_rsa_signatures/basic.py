from toy_cryptography.plain_rsa_signatures import signature_for
from toy_cryptography.plain_rsa_signatures.keys import *


private_key = determine_private_key(
    prime1=278_087,
    prime2=115_903,
    public_exponent=31,
)
message = 1234567890
signature = signature_for(message, private_key)


def main():
    print(f"{private_key.modulus = }")
    print(f"{message = }")
    print(f"{signature = }")


if __name__ == '__main__':
    main()
