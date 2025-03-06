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

import asyncio
import base64
from urllib.parse import unquote_plus as urlunquote, quote_plus as urlquote

import aiohttp

from utils.padding_oracle_crack import PaddingOracleCracker

service_origin = "http://localhost:3000"
# service_origin = "http://challenge.ctf.games:31283"  # from https://snyk.ctf.games/challenges


async def get_token(session: aiohttp.ClientSession) -> (bytes, bytes):
    response = await session.get(f"{service_origin}/api/token")
    body = await response.json()
    token_base64_urlencoded = body["token"]
    token_base64 = urlunquote(token_base64_urlencoded)
    token = base64.b64decode(token_base64)
    iv, ciphertext = bytearray(token[:16]), bytearray(token[16:])
    return iv, ciphertext


async def try_token(session: aiohttp.ClientSession, iv: bytes, ciphertext: bytes) -> bool:
    token_base64 = base64.b64encode(iv + ciphertext).decode("utf-8")
    token_base64_urlencoded = urlquote(token_base64)
    response = await session.post(f"{service_origin}/api/submit/{token_base64_urlencoded}")
    body = await response.json()
    if body["error"] == 'Missing code in request body':
        return True
    return False


async def sanity_check():
    async with aiohttp.ClientSession() as session:
        iv, ciphertext = await get_token(session)
        assert await try_token(session, iv, ciphertext)


asyncio.run(sanity_check())


async def main():
    async def oracle(iv: bytes, ciphertext: bytes) -> bool:
        nonlocal session
        return await try_token(session, iv, ciphertext)

    async with aiohttp.ClientSession() as session:
        iv, ciphertext = await get_token(session)
        cracker = PaddingOracleCracker(iv, ciphertext, oracle)
        plaintext = await cracker.crack_plaintext()
    print(plaintext.decode("utf-8"))


if __name__ == "__main__":
    asyncio.run(main())
