import asyncio

from utils.wordlists import *


async def main():
    async with word_list("bip-39") as bip39:
        phrases = [random_phrase(bip39, 3) for _ in range(10)]

    print(phrases)


if __name__ == "__main__":
    asyncio.run(main())
