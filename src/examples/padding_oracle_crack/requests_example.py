"""
This example is a partial solution to a past CTF challenge:
- 'Padding Gambit', Snyk Fetch the Flag 2025

in the challenge, a Node.js server would
- supply a 'token' (AES-128-CBC encrypted IV+ciphertext) via one endpoint
- accept requests including the token via another endpoint

since the latter endpoint would provide a different response depending on the validity
of the provided token, it could be used to construct a 'padding oracle' which would allow
decryption of the 'token' without knowledge of the encryption secret.
"""

import base64
from urllib.parse import unquote_plus as urlunquote, quote_plus as urlquote

import requests

from utils.padding_oracle_crack import PaddingOracleCracker


my_token_base64 = urlunquote("fCHta4KM9gOTBkQCGinmuuogytHDRrl%2F7g032l7VSOrVeH939p04HWFrP9Jrf%2B4CInfqkWjX1d8rS8o0HXP4rQ%3D%3D")
my_token = base64.b64decode(my_token_base64)
iv, ciphertext = bytearray(my_token[:16]), bytearray(my_token[16:])


def try_token(iv: bytes, ciphertext: bytes) -> bool:
    token_base64 = base64.b64encode(iv + ciphertext).decode("utf-8")
    token_base64_urlencoded = urlquote(token_base64)
    response = requests.post(f"http://localhost:3000/api/submit/{token_base64_urlencoded}")
    body = response.json()
    if body["error"] == 'Missing code in request body':
        return True
    return False


assert try_token(iv, ciphertext)


def main():
    cracker = PaddingOracleCracker(iv, ciphertext, try_token)
    plaintext = cracker.crack_plaintext()
    print(plaintext.decode("utf-8"))


if __name__ == "__main__":
    main()
