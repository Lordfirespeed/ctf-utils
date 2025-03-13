"""
This example is a partial solution to a past CTF challenge:
- 'Padding Gambit', Snyk Fetch the Flag 2025

After the first stage (see examples/padding_oracle_crack/aiohttp_example.py), the player
obtains as pastebin link: https://pastebin.com/rzZMdkvs.

Its contents:
```
would you like to play a game? 1PPPP3/2P1P3/1P3PP1/1PPP1P2/1P3PP1/2PP2P1/2PP1P1P/2P1P2P w - - 0 1
```

This is 'Forsyth–Edwards' notation for a chess game position.
Players had to
- parse the notation to build the game state
- observe that the board consists only of empty space and white pawns, and the position is very unusual
- 'chaining' the ranks (rows) of the board together, interpret empty squares as '0' and inhabited squares as '1'
  to build a binary string
- decode the binary string to obtain a plaintext, which could be given to the Node.js server from the first
  stage in exchange for the flag.
"""
from itertools import chain
from typing import Iterable

from utils.binary_extras import byte_length
from utils.miscellaneous import ChessGamePosition


game_state_notation = "1PPPP3/2P1P3/1P3PP1/1PPP1P2/1P3PP1/2PP2P1/2PP1P1P/2P1P2P w - - 0 1"
game = ChessGamePosition.from_notation(game_state_notation)


def truth_sequence_to_binary(sequence: Iterable[object]) -> str:
    return "0b" + "".join("0" if item is None else "1" for item in sequence)


def binary_literal_to_bytes(binary_literal: str) -> bytes:
    value = int(binary_literal, 2)
    value_byte_length = byte_length(value)
    return value.to_bytes(length=value_byte_length)


def main():
    game.pretty_print_board()
    print(game)

    board_tile_grid = game.board
    board_tile_sequence = chain(*board_tile_grid)
    board_binary_string = truth_sequence_to_binary(board_tile_sequence)
    print(f"{board_binary_string = !s}")
    board_bytes = binary_literal_to_bytes(board_binary_string)
    print(f"{board_bytes = }")


if __name__ == "__main__":
    main()
