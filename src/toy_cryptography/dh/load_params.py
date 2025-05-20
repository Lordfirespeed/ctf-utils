from pathlib import Path

from cryptography.hazmat.primitives.serialization import (
    load_pem_parameters as parse_pem_parameters,
)

from toy_cryptography.dh.params import DiffieHellmanParams


def load_pem_dh_parameters(parameters_file: Path) -> DiffieHellmanParams:
    """
    ```bash
    openssl genpkey -genparam -algorithm dh -out dhparams.pem
    ```
    """
    with open(parameters_file, "rb") as parameters_file_handle:
        data = parameters_file_handle.read()
    parsed_parameters = parse_pem_parameters(data)
    numbers = parsed_parameters.parameter_numbers()
    return DiffieHellmanParams(prime=numbers.p, generator=numbers.g)


__all__ = ("load_pem_dh_parameters",)
