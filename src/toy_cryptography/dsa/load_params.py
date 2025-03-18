from base64 import b64decode
from pathlib import Path

from pyasn1.codec.der.decoder import decode as asn1decode
from pyasn1.type.univ import Sequence, Integer
from pyasn1.type.namedtype import NamedTypes, NamedType

from utils import pem

from .params import DSAParams


class DSAParamsSchema(Sequence):
    """
    ASN.1 specification:

    DSAParams ::= SEQUENCE {
        P    INTEGER,
        Q    INTEGER,
        G    INTEGER
    }
    """
    componentType = NamedTypes(
        NamedType("P", Integer()),
        NamedType("Q", Integer()),
        NamedType("G", Integer()),
    )


def load_pem_dsa_parameters(parameters_file: Path) -> DSAParams:
    """
    ```bash
    openssl genpkey -genparam -algorithm dsa -out params.pem
    ```
    """
    with open(parameters_file, "rb") as parameters_file_handle:
        data = parameters_file_handle.read()
    pem_objects = pem.parse(data)
    assert len(pem_objects) == 1
    parameters_object = pem_objects[0]
    assert parameters_object.identifier == b"DSA PARAMETERS"
    payload = b64decode(parameters_object.content)
    result, _ = asn1decode(payload, DSAParamsSchema())
    return DSAParams(
        p=int(result["P"]),
        q=int(result["Q"]),
        g=int(result["G"]),
    )


__all__ = ("load_pem_dsa_parameters",)
