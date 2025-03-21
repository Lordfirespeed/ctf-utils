import asyncio
import itertools
import json
from pathlib import Path
from string import ascii_lowercase
from typing import Iterator, Mapping

from yarl import URL

from definitions import project_cache_dirname
from extras.collections_extras import sortabledict
from utils.cached_download import cached_download


async def ensure_main_bigrams_dataset_file() -> Path:
    return await cached_download(
        URL("https://raw.githubusercontent.com/sekaha/Ngram_Frequency_Graphs/refs/heads/main/bigrams.txt"),
        Path("bigrams.txt"),
    )


def load_txt_bigrams_dataset(dataset_file: Path) -> Mapping[str, int]:
    bigrams_dataset = sortabledict[str, int]()
    with open(dataset_file) as bigrams_dataset_file_handle:
        for line in bigrams_dataset_file_handle:
            bigram, frequency_str = line.rstrip().split("\t")
            bigrams_dataset[bigram] = int(frequency_str)
    bigrams_dataset.sort()
    return dict(bigrams_dataset)


def load_json_bigrams_dataset(dataset_file: Path) -> Mapping[str, int]:
    with open(dataset_file) as bigrams_dataset_file_handle:
        contents = json.load(bigrams_dataset_file_handle)
    assert isinstance(contents, dict)
    return contents  # implicit unchecked assignment here


async def load_main_bigrams_dataset() -> Mapping[str, int]:
    main_bigrams_dataset_file = await ensure_main_bigrams_dataset_file()
    return load_txt_bigrams_dataset(main_bigrams_dataset_file)


def compute_lowercase_bigrams_dataset(main_bigrams_dataset: Mapping[str, int]) -> Mapping[str, int]:
    def all_lowercase_bigrams() -> Iterator[str]:
        for pair in itertools.product(ascii_lowercase + " ", repeat=2):
            yield "".join(pair)

    lowercase_bigrams_dataset = sortabledict[str, int]({ bigram: 0 for bigram in all_lowercase_bigrams() })

    for bigram, frequency in main_bigrams_dataset.items():
        left, right = bigram
        if not (left.islower() or left.isspace()):
            continue
        if not (right.islower() or right.isspace()):
            continue
        lowercase_bigrams_dataset[bigram] = frequency

    lowercase_bigrams_dataset.sort()
    return dict(lowercase_bigrams_dataset)


def compute_no_spaces_lowercase_bigrams_dataset(main_bigrams_dataset: Mapping[str, int]) -> Mapping[str, int]:
    def all_lowercase_bigrams() -> Iterator[str]:
        for pair in itertools.product(ascii_lowercase, repeat=2):
            yield "".join(pair)

    no_spaces_lowercase_bigrams_dataset = sortabledict[str, int]({ bigram: 0 for bigram in all_lowercase_bigrams() })

    for bigram, frequency in main_bigrams_dataset.items():
        left, right = bigram
        if not left.islower():
            continue
        if not right.islower():
            continue
        no_spaces_lowercase_bigrams_dataset[bigram] = frequency

    no_spaces_lowercase_bigrams_dataset.sort()
    return dict(no_spaces_lowercase_bigrams_dataset)


async def ensure_lowercase_bigrams_dataset_file() -> Path:
    dataset_file = project_cache_dirname / "lowercase-bigrams-with-spaces.json"
    if dataset_file.exists():
        return dataset_file

    main_bigrams_dataset = await load_main_bigrams_dataset()
    lowercase_bigrams_dataset = compute_lowercase_bigrams_dataset(main_bigrams_dataset)
    with open(dataset_file, "w") as dataset_file_handle:
        json.dump(lowercase_bigrams_dataset, dataset_file_handle, indent=2)

    return dataset_file


async def ensure_no_spaces_lowercase_bigrams_dataset_file() -> Path:
    dataset_file = project_cache_dirname / "lowercase-bigrams-without-spaces.json"
    if dataset_file.exists():
        return dataset_file

    main_bigrams_dataset = await load_main_bigrams_dataset()
    no_spaces_lowercase_bigrams_dataset = compute_no_spaces_lowercase_bigrams_dataset(main_bigrams_dataset)
    with open(dataset_file, "w") as dataset_file_handle:
        json.dump(no_spaces_lowercase_bigrams_dataset, dataset_file_handle, indent=2)

    return dataset_file


async def load_lowercase_bigrams_dataset() -> Mapping[str, int]:
    lowercase_bigrams_dataset_file = await ensure_lowercase_bigrams_dataset_file()
    return load_json_bigrams_dataset(lowercase_bigrams_dataset_file)


async def load_no_spaces_lowercase_bigrams_dataset() -> Mapping[str, int]:
    no_spaces_lowercase_bigrams_dataset_file = await ensure_no_spaces_lowercase_bigrams_dataset_file()
    return load_json_bigrams_dataset(no_spaces_lowercase_bigrams_dataset_file)


async def main():
    await ensure_main_bigrams_dataset_file()
    await ensure_lowercase_bigrams_dataset_file()


__all__ = (
    "load_main_bigrams_dataset",
    "load_lowercase_bigrams_dataset",
    "load_no_spaces_lowercase_bigrams_dataset",
)

if __name__ == "__main__":
    asyncio.run(main())
