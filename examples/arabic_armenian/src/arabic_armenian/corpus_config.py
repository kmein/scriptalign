"""Load the bundled Arabic-Armenian word list into a :class:`ParallelCorpus`."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Mapping

from scriptalign import ParallelCorpus, load_parallel_corpus

from .orthographies import ARABIC, ARMENIAN

ARMENIAN_COLUMN = "Armenian"
ARABIC_COLUMN = "Arabic"


def default_data_path() -> Path:
    """Path to the CSV bundled with this package."""
    return Path(str(resources.files(__package__).joinpath("words.csv")))


def _row_filter(row: Mapping[str, str]) -> dict[str, str] | None:
    # Skip rows where either side is missing (the table has dash-only rows).
    armenian = row.get(ARMENIAN_COLUMN, "").strip()
    arabic = row.get(ARABIC_COLUMN, "").strip()
    if not armenian or not arabic or armenian == "–" or arabic == "–":
        return None
    return dict(row)


def load_corpus(csv_path: str | Path | None = None) -> ParallelCorpus:
    return load_parallel_corpus(
        csv_path if csv_path is not None else default_data_path(),
        column_a=ARMENIAN_COLUMN,
        column_b=ARABIC_COLUMN,
        script_a=ARMENIAN,
        script_b=ARABIC,
        row_filter=_row_filter,
    )
