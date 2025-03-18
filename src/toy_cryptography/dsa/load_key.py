from pathlib import Path

from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key as parse_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric import dsa as pyca_dsa

from .keys import DSAPrivateKey
from .params import DSAParams


def load_pem_dsa_private_key(key_file: Path) -> DSAPrivateKey:
    """
    ```bash
    openssl genpkey -paramfile dsaparams.pem -out dsakey.pem
    ```
    """
    with open(key_file, "rb") as parameters_file_handle:
        data = parameters_file_handle.read()
    parsed_key = parse_pem_private_key(data, None)
    assert isinstance(parsed_key, pyca_dsa.DSAPrivateKey)
    private_numbers = parsed_key.private_numbers()
    public_numbers = private_numbers.public_numbers
    parameter_numbers = public_numbers.parameter_numbers
    params = DSAParams(
        parameter_numbers.p,
        parameter_numbers.q,
        parameter_numbers.g,
    )
    return DSAPrivateKey(
        private_numbers.x,
        public_numbers.y,
        params,
    )


__all = ("load_pem_dsa_private_key",)
