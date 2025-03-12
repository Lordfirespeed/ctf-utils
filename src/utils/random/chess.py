"""
https://en.m.wikipedia.org/wiki/Forsyth-Edwards_Notation
"""
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Iterable, Literal, Self, TypeGuard
from enum import StrEnum, Flag

from utils.ansi import StyleEscapeBuilder, StyleOrdinal
from utils.ansi.styles import reset_all as style_reset


type ChessPieceString = Literal["P"]
type ChessSquareInhabitant = ChessPieceString | None
type ChessBoard = list[list[ChessSquareInhabitant]]
type RankCoordinate = Literal[1, 2, 3, 4, 5, 6, 7, 8]
type FileCoordinate = Literal["a", "b", "c", "d", "e", "f", "g", "h"]


class ChessColour(StrEnum):
    white = "white"
    black = "black"

    @classmethod
    def from_notation(cls, colour_notation_string: str) -> Self:
        assert len(colour_notation_string) == 1
        if colour_notation_string == "w":
            return cls.white
        if colour_notation_string == "b":
            return cls.black
        raise Exception(f"Unrecognised notation {colour_notation_string!r} in active colour notation")


class ChessCastlingAvailability(Flag):
    none = 0
    white_can_castle_kingside = 1 << 0
    white_can_castle_queenside = 1 << 1
    black_can_castle_kingside = 1 << 2
    black_can_castle_queenside = 1 << 3

    @classmethod
    def from_notation(cls, castling_availability_notation_string: str) -> Self:
        assert len(castling_availability_notation_string) <= 4
        if castling_availability_notation_string == "-":
            return cls.none

        castling_availability = cls.none
        for character in castling_availability_notation_string:
            if character == "K":
                castling_availability |= cls.white_can_castle_kingside
                continue
            if character == "Q":
                castling_availability |= cls.white_can_castle_queenside
                continue
            if character == "k":
                castling_availability |= cls.black_can_castle_kingside
                continue
            if character == "q":
                castling_availability |= cls.black_can_castle_queenside
                continue
            raise Exception(f"Unrecognised character {character!r} in castling availability notation")
        return castling_availability


@dataclass(frozen=True)
class ChessSquareReference:
    file: FileCoordinate
    rank: RankCoordinate

    @classmethod
    def from_indexes(cls, file_index: int, rank_index: int) -> Self:
        file_coordinate = chr(97 + file_index)
        rank_coordinate = 8 - rank_index
        return cls(file_coordinate, rank_coordinate)

    @classmethod
    def from_notation(cls, square_notation_string: str) -> Self | None:
        if square_notation_string == "-":
            return None
        assert len(square_notation_string) == 2
        file_coordinate, rank_coordinate_string = square_notation_string
        rank_coordinate = int(rank_coordinate_string)
        return cls(file_coordinate, rank_coordinate)

    def __init__(self, file: str, rank: int):
        file = file.lower()
        assert is_file_coordinate(file)
        assert is_rank_coordinate(rank)

        object.__setattr__(self, "file", file)
        object.__setattr__(self, "rank", rank)

    def __str__(self):
        return f"{self.file}{self.rank}"

    @property
    def file_index(self) -> int:
        return ord(self.file) - 97

    @property
    def rank_index(self) -> int:
        return 8 - self.rank


def is_rank_coordinate(rank_int: int) -> TypeGuard[RankCoordinate]:
    return 1 <= rank_int <= 8


file_str_set = set("abcdefgh")
def is_file_coordinate(file_str: str) -> TypeGuard[FileCoordinate]:
    if len(file_str) != 1: return False
    return "a" <= file_str <= "h"


def is_chess_piece_string(piece_string: str) -> TypeGuard[ChessPieceString]:
    return piece_string == "P"


def parse_rank_notation(rank_notation_string: str) -> list[ChessSquareInhabitant]:
    rank: list[ChessSquareInhabitant] = []

    def add_empty_space(length: int) -> None:
        nonlocal rank
        rank += [None] * length

    def add_piece(piece: ChessPieceString) -> None:
        nonlocal rank
        rank.append(piece)

    for character in rank_notation_string:
        if character.isnumeric():
            add_empty_space(int(character))
            continue

        if is_chess_piece_string(character):
            add_piece(character)
            continue

        raise Exception(f"unrecognised piece notation: {character}")

    assert len(rank) == 8
    return rank


def parse_board_notation(board_notation_string: str) -> ChessBoard:
    rank_notation_strings = board_notation_string.split("/")
    assert len(rank_notation_strings) == 8
    return [parse_rank_notation(rank_notation_string) for rank_notation_string in rank_notation_strings]


white_text_on_black = StyleEscapeBuilder() \
    .argue(StyleOrdinal.bright_white_foreground) \
    .argue(StyleOrdinal.black_background) \
    .finalize()
black_text_on_white = StyleEscapeBuilder() \
    .argue(StyleOrdinal.black_foreground) \
    .argue(StyleOrdinal.bright_white_background) \
    .finalize()


def chequered(square: ChessSquareReference) -> str:
    # a1 is a dark tile -> a8 is a light tile -> (0,0) is a light tile
    parity = pow(-1, square.rank_index + square.file_index)
    if parity == 1:
        return black_text_on_white  # light tile
    else:
        return white_text_on_black  # dark tile


@dataclass(frozen=True)
class ChessGamePosition:
    _board: ChessBoard = field(repr=False)
    active_colour: ChessColour
    castling_availability: ChessCastlingAvailability
    en_passant_square: ChessSquareReference | None
    halfmove_clock: int
    fullmove_number: int

    @classmethod
    def from_notation(cls, state_notation_string: str) -> Self:
        state_notation_string_parts = state_notation_string.split()
        assert len(state_notation_string_parts) == 6
        board_notation_string = state_notation_string_parts[0]
        active_colour_notation_string = state_notation_string_parts[1]
        castling_availability_notation_string = state_notation_string_parts[2]
        en_passant_square_notation_string = state_notation_string_parts[3]
        halfmove_clock_notation_string = state_notation_string_parts[4]
        fullmove_number_notation_string = state_notation_string_parts[5]

        return cls(
            parse_board_notation(board_notation_string),
            ChessColour.from_notation(active_colour_notation_string),
            ChessCastlingAvailability.from_notation(castling_availability_notation_string),
            ChessSquareReference.from_notation(en_passant_square_notation_string),
            int(halfmove_clock_notation_string),
            int(fullmove_number_notation_string),
        )

    @property
    def board(self):
        return deepcopy(self._board)

    def __getitem__(self, item: ChessSquareReference) -> ChessSquareInhabitant:
        assert isinstance(item, ChessSquareReference)
        return self._board[item.rank_index][item.file_index]

    def pretty_render_board(self) -> str:
        def render_square_inhabitant(inhabitant: ChessSquareInhabitant) -> str:
            if inhabitant is None: return " "
            return inhabitant

        def render_square(square: ChessSquareReference) -> str:
            square_style = chequered(square)
            inhabitant = self[square]
            return f"{square_style}{render_square_inhabitant(inhabitant):^3}"

        def rendered_squares_in_rank(rank_index: int) -> Iterable[str]:
            for file_index in range(8):
                square = ChessSquareReference.from_indexes(file_index, rank_index)
                yield render_square(square)

        def render_rank(rank_index: int) -> str:
            rank_coordinate = 8 - rank_index
            rendered_rank_interior = "".join(rendered_squares_in_rank(rank_index))
            return f"{rank_coordinate} {rendered_rank_interior}{style_reset}"

        def rendered_file_labels() -> Iterable[str]:
            for file_coordinate in "abcdefgh":
                yield f"{file_coordinate:^3}"

        def render_file_labels() -> str:
            padding = f"{'':2}"
            return f"{padding}{"".join(rendered_file_labels())}"

        def lines_of_rendered_board() -> Iterable[str]:
            for rank_index in range(8):
                yield render_rank(rank_index)
            yield render_file_labels()

        def render_board() -> str:
            return "\n".join(lines_of_rendered_board())

        return render_board()

    def pretty_print_board(self) -> None:
        print(self.pretty_render_board())
