from dataclasses import dataclass
import functools

from utils.ansi.styles import bright_magenta_foreground as pink, reset_all as style_reset


@dataclass(frozen=True)
class CommonSubsequence:
    content: str
    of_first: str
    of_second: str
    first_indexes: tuple[int]
    second_indexes: tuple[int]

    def __post_init__(self):
        assert len(self.content) == len(self.first_indexes) == len(self.second_indexes)
        for content_index in range(len(self.content)):
            first_index = self.first_indexes[content_index]
            second_index = self.second_indexes[content_index]
            assert self.content[content_index] == self.of_first[first_index] == self.of_second[second_index]

    def _render_start_segment(self) -> (str, str, str):
        to_first_index = self.first_indexes[0]
        to_second_index = self.second_indexes[0]
        left_pad_to_length: int = max(to_first_index, to_second_index)
        highlighted_character = f"{pink}{self.content[0]}{style_reset}"
        cruft_of_first = self.of_first[:to_first_index]
        cruft_of_second = self.of_second[:to_second_index]

        segment_of_first = f"{cruft_of_first:^{left_pad_to_length}}{highlighted_character}"
        segment_of_second = f"{cruft_of_second:^{left_pad_to_length}}{highlighted_character}"
        segment_of_pointer = f"{'':>{left_pad_to_length}}{pink}^{style_reset}"
        return segment_of_first, segment_of_second, segment_of_pointer

    def _render_middle_segment(self, segment_index: int) -> (str, str, str):
        assert segment_index > 0
        from_first_index = self.first_indexes[segment_index - 1] + 1
        from_second_index = self.second_indexes[segment_index - 1] + 1
        to_first_index = self.first_indexes[segment_index]
        to_second_index = self.second_indexes[segment_index]
        left_pad_to_length: int = max(to_first_index - from_first_index, to_second_index - from_second_index)
        highlighted_character = f"{pink}{self.content[segment_index]}{style_reset}"
        cruft_of_first = self.of_first[from_first_index:to_first_index]
        cruft_of_second = self.of_second[from_second_index:to_second_index]

        segment_of_first = f"{cruft_of_first:^{left_pad_to_length}}{highlighted_character}"
        segment_of_second = f"{cruft_of_second:^{left_pad_to_length}}{highlighted_character}"
        segment_of_pointer = f"{'':>{left_pad_to_length}}{pink}^{style_reset}"
        return segment_of_first, segment_of_second, segment_of_pointer

    def _render_final_segment(self) -> (str, str, str):
        from_first_index = self.first_indexes[-1] + 1
        from_second_index = self.second_indexes[-1] + 1
        cruft_of_first = self.of_first[from_first_index:]
        cruft_of_second = self.of_second[from_second_index:]
        segment_of_first = f"{cruft_of_first}"
        segment_of_second = f"{cruft_of_second}"
        segment_of_pointer = ""
        return segment_of_first, segment_of_second, segment_of_pointer

    def pretty_print(self):
        segment_tuples = [
            self._render_start_segment(),
            *(self._render_middle_segment(index) for index in range(1, len(self.content))),
            self._render_final_segment(),
        ]

        # 'transpose' i.e. [(1, 2), (3, 4), (5, 6), (7, 8)] -> [(1, 3, 5, 7), (2, 4, 6, 8)]
        segments_of_first, segments_of_second, segments_of_pointer = list(zip(*segment_tuples))

        print("".join(segments_of_first))
        print("".join(segments_of_second))
        print("".join(segments_of_pointer))


@functools.cache
def _longest_common_subsequence(a: str, b: str) -> (str, (..., int), (..., int)):
    """
    :return tuple of `(best, best_a_indexes, best_b_indexes)`, where `best` is the longest common subsequence
    and the indexes locate the subsequence in `a` and `b` (respectively).
    """
    best: str = ""
    best_a_indexes: (..., int) = tuple()
    best_b_indexes: (..., int) = tuple()

    if len(a) == 0 or len(b) == 0:
        return best, best_a_indexes, best_b_indexes

    def consider(common_substring: str, a_indexes: (..., int), b_indexes: (..., int)) -> None:
        nonlocal best, best_a_indexes, best_b_indexes
        if len(common_substring) <= len(best):
            return
        best = common_substring
        best_a_indexes = a_indexes
        best_b_indexes = b_indexes

    # it's possible an early-return in this branch would not break the correctness of the algorithm, but I can't
    # remember at time of writing this, so using `consider()` to be safe
    if a[0] == b[0]:
        special_case_best, special_case_best_a_indexes, special_case_best_b_indexes = _longest_common_subsequence(a[1:], b[1:])
        special_case_best = a[0] + special_case_best
        special_case_best_a_indexes = (0, *(index + 1 for index in special_case_best_a_indexes))
        special_case_best_b_indexes = (0, *(index + 1 for index in special_case_best_b_indexes))
        consider(special_case_best, special_case_best_a_indexes, special_case_best_b_indexes)

    case_one_best, case_one_best_a_indexes, case_one_best_b_indexes = _longest_common_subsequence(a[1:], b)
    case_one_best_a_indexes = tuple(index + 1 for index in case_one_best_a_indexes)
    consider(case_one_best, case_one_best_a_indexes, case_one_best_b_indexes)

    case_two_best, case_two_best_a_indexes, case_two_best_b_indexes = _longest_common_subsequence(a, b[1:])
    case_two_best_b_indexes = tuple(index + 1 for index in case_two_best_b_indexes)
    consider(case_two_best, case_two_best_a_indexes, case_two_best_b_indexes)

    return best, best_a_indexes, best_b_indexes


def longest_common_subsequence(a: str, b: str) -> CommonSubsequence:
    best, best_a_indexes, best_b_indexes = _longest_common_subsequence(a, b)

    return CommonSubsequence(
        content=best,
        of_first=a,
        of_second=b,
        first_indexes=best_a_indexes,
        second_indexes=best_b_indexes,
    )


def main():
    my_email = "me@lordfirespeed.dev"
    my_password = "dethrone1earldom.colorings@HARPOON0insider"  # not a password I actually use for anything :)

    result = longest_common_subsequence(my_email, my_password)
    result.pretty_print()


__all__ = ("CommonSubsequence", "longest_common_subsequence",)


if __name__ == "__main__":
    main()
