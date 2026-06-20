"""Disk I/O helpers — separate from the pure algorithmic core."""

from __future__ import annotations

import csv
import pickle
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from .corpus import ParallelCorpus


def save_matrix_csv(path: str | Path, matrix: np.ndarray) -> None:
    np.savetxt(path, matrix, delimiter=",")


def save_labeled_matrix_csv(
    path: str | Path,
    matrix: np.ndarray,
    row_labels: Sequence[str],
    col_labels: Sequence[str],
) -> None:
    """Write ``matrix`` as a CSV with letter headers across the top and letter
    labels down the first column. Suited to opening in a spreadsheet."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([""] + list(col_labels))
        for label, row in zip(row_labels, matrix):
            writer.writerow([label] + [f"{v:.12f}" for v in row])


def save_correspondences_tsv(
    path: str | Path,
    matrix: np.ndarray,
    row_labels: Sequence[str],
    col_labels: Sequence[str],
) -> None:
    """Write every letter pair on its own line, sorted strongest-correlated
    first. Three tab-separated columns: ``a``, ``b``, ``phi``."""
    from .formatting import rank_correspondences

    with open(path, "w") as f:
        f.write("a\tb\tphi\n")
        for value, a, b in rank_correspondences(matrix, row_labels, col_labels):
            f.write(f"{a}\t{b}\t{value:+.6f}\n")


def save_state(
    path: str | Path,
    corpus: ParallelCorpus,
    alignments: list[list[tuple[int, int]]],
) -> None:
    """Persist the current corpus + alignments to a pickle.

    The schema is dict-keyed (``words_a``, ``words_b``, ``alignments``) and
    domain-neutral. See :func:`load_legacy_state` for reading the original
    Coptic-Arabic ``aligned_texts.p`` shape.
    """
    payload = {
        "words_a": corpus.words_a,
        "words_b": corpus.words_b,
        "alignments": [list(a) for a in alignments],
    }
    with open(path, "wb") as f:
        pickle.dump(payload, f)


def load_state(path: str | Path) -> dict[str, Any]:
    with open(path, "rb") as f:
        return pickle.load(f)


def load_legacy_state(path: str | Path) -> dict[str, Any]:
    """Read the historic ``aligned_texts.p`` whose keys were ``Coptic`` /
    ``Arabic`` / ``Alignments``. Returns a dict in the new schema."""
    with open(path, "rb") as f:
        legacy = pickle.load(f)
    return {
        "words_a": legacy["Coptic"],
        "words_b": legacy["Arabic"],
        "alignments": legacy["Alignments"],
    }
