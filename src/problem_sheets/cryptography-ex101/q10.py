from toy_cryptography.dh.params import DiffieHellmanParams
from toy_cryptography.dh.scheme import *


params = DiffieHellmanParams(prime=17, generator=3)
alice_key = DHPrivateKey(5)
bob_key = DHPrivateKey(11)

alice_public_exponent = derive_public_key(params, alice_key)
bob_public_exponent = derive_public_key(params, bob_key)

alice_shared_secret = derive_shared_secret_key(params, alice_key, bob_public_exponent)
bob_shared_secret = derive_shared_secret_key(params, bob_key, alice_public_exponent)


def main():
    print(f"1a) Alice selects their private group element a = {alice_key}")
    print(f"1b) Bob selects their private group element b = {bob_key}")
    print(f"2a) Alice sends their public exponent A = g^a = {alice_public_exponent} to Bob")
    print(f"2b) Bob sends their public exponent B = g^b = {bob_public_exponent} to Alice")
    print(f"3a) Alice computes their shared secret B^a = {alice_shared_secret} = g^(ab)")
    print(f"3b) Bob computes their shared secret A^b = {bob_shared_secret} = g^(ab)")


if __name__ == "__main__":
    main()
