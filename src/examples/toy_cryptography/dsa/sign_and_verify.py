from toy_cryptography.dsa import DSAScheme, DSAParams, determine_params, gen_private_key


def hash_function(group_element: int, params: DSAParams) -> int:
    return pow(group_element, 3, mod=params.q)


def main() -> None:
    params = determine_params(
        2 * 8720429 + 1,
        8720429,
    )
    private_key = gen_private_key(params)
    public_key = private_key.extract_public_key()

    scheme = DSAScheme(hash_function)
    message = 0b1100110011001100
    signature = scheme.signature_for(message, private_key)
    valid = scheme.verify_signature(message, signature, public_key)
    print(f"the signature is {"valid" if valid else "invalid"}")


if __name__ == "__main__":
    main()
