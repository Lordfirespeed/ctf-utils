from pathlib import Path

from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key as parse_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric import rsa as pyca_rsa

from .keys import RSAPrivateKey


def load_pem_rsa_private_key(key_file: Path) -> RSAPrivateKey:
    """
    ```bash
    openssl genpkey -algorithm rsa -out rsakey.pem
    ```
    """
    with open(key_file, "rb") as parameters_file_handle:
        data = parameters_file_handle.read()
    parsed_key = parse_pem_private_key(data, None)
    assert isinstance(parsed_key, pyca_rsa.RSAPrivateKey)
    private_numbers = parsed_key.private_numbers()
    public_numbers = private_numbers.public_numbers
    return RSAPrivateKey(
        modulus=public_numbers.n,
        public_exponent=public_numbers.e,
        private_exponent=private_numbers.d,

        prime1=private_numbers.p,
        prime2=private_numbers.q,
        private_exponent1=private_numbers.dmp1,
        private_exponent2=private_numbers.dmq1,
        coefficient=private_numbers.iqmp,
    )


__all__ = ("load_pem_rsa_private_key",)
