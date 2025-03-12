from dataclasses import dataclass
import functools

from utils import colours


@dataclass(frozen=True)
class CommonSubstring:
    content: str
    of_first: str
    of_second: str
    first_index: slice
    second_index: slice

    def __post_init__(self):
        assert self.content == self.of_first[self.first_index]
        assert self.content == self.of_second[self.second_index]

    def pretty_print(self):
        left_pad_to_length: int = max(self.first_index.start, self.second_index.start)

        highlighted_substring = f"{colours.pink}{self.content}{colours.reset}"
        start_of_first = self.of_first[:self.first_index.start]
        end_of_first = self.of_first[self.first_index.stop:]
        start_of_second = self.of_second[:self.second_index.start]
        end_of_second = self.of_second[self.second_index.stop:]

        print(f"{start_of_first:>{left_pad_to_length}}{highlighted_substring}{end_of_first}")
        print(f"{start_of_second:>{left_pad_to_length}}{highlighted_substring}{end_of_second}")
        print(f"{'':>{left_pad_to_length}}{colours.pink}{'^' * len(self.content)}{colours.reset}")


@functools.cache
def _longest_left_aligned_common_substring(a: str, b: str) -> str:
    cursor = 0
    while True:
        if cursor >= len(a): break
        if cursor >= len(b): break
        if a[cursor] != b[cursor]: break
        cursor += 1
    return a[:cursor]


@functools.cache
def _longest_common_substring(a: str, b: str) -> (str, int, int):
    """
    :return tuple of `(best, best_a_start_index, best_b_start_index)`, where `best` is the longest common substring
    and the indexes locate the substring in `a` and `b` (respectively).
    """
    best: str = ""
    best_a_start_index: int = 0
    best_b_start_index: int = 0

    if len(a) == 0 or len(b) == 0:
        return best, best_a_start_index, best_b_start_index

    def consider(common_substring: str, a_start_index: int, b_start_index: int) -> None:
        nonlocal best, best_a_start_index, best_b_start_index
        if len(common_substring) <= len(best):
            return
        best = common_substring
        best_a_start_index = a_start_index
        best_b_start_index = b_start_index

    consider(_longest_left_aligned_common_substring(a, b), 0, 0)

    case_one_best, case_one_best_a_start_index, case_one_best_b_start_index = _longest_common_substring(a[1:], b)
    case_one_best_a_start_index += 1
    consider(case_one_best, case_one_best_a_start_index, case_one_best_b_start_index)

    case_two_best, case_two_best_a_start_index, case_two_best_b_start_index = _longest_common_substring(a, b[1:])
    case_two_best_b_start_index += 1
    consider(case_two_best, case_two_best_a_start_index, case_two_best_b_start_index)

    return best, best_a_start_index, best_b_start_index


def longest_common_substring(a: str, b: str) -> CommonSubstring:
    best, best_a_start_index, best_b_start_index = _longest_common_substring(a, b)
    best_a_index = slice(best_a_start_index, best_a_start_index + len(best))
    best_b_index = slice(best_b_start_index, best_b_start_index + len(best))
    return CommonSubstring(
        content=best,
        of_first=a,
        of_second=b,
        first_index=best_a_index,
        second_index=best_b_index,
    )


def main():
    my_email = "me@lordfirespeed.dev"
    my_password = "dethrone1earldom.colorings@HARPOON0insider"  # not a password I actually use for anything :)

    result = longest_common_substring(my_email, my_password)
    result.pretty_print()


if __name__ == "__main__":
    main()
