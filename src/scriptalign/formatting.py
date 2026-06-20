"""Human-readable views of alignments and scoring matrices."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np

from .em import AlignmentResult


def format_word_alignment(
    word_a: str,
    word_b: str,
    alignment: Sequence[tuple[int, int]],
) -> str:
    """Render a single word's alignment as a four-row tab-separated block:
    indices in B, letters in B, letters in A, indices in A.

    Matches the layout produced by the legacy ``improve_alignment.py``.
    """
    idx_a = [str(p[0]) for p in alignment]
    idx_b = [str(p[1]) for p in alignment]
    chars_a = [word_a[p[0]] for p in alignment]
    chars_b = [word_b[p[1]] for p in alignment]
    rows = ["\t".join(chars_b), "\t".join(idx_b), "\t".join(idx_a), "\t".join(chars_a)]
    return "\n".join(rows)


def rank_correspondences(
    phi: np.ndarray,
    alphabet_a: Sequence[str],
    alphabet_b: Sequence[str],
) -> list[tuple[float, str, str]]:
    """Every letter pair, sorted strongest-correlated first.

    Returns ``(phi, letter_a, letter_b)`` triples. The sort is stable on
    Python's iteration order over ``(i, j)``, so re-running on the same
    matrix produces an identical sequence.
    """
    return sorted(
        (
            (float(phi[i, j]), alphabet_a[i], alphabet_b[j])
            for i in range(phi.shape[0])
            for j in range(phi.shape[1])
        ),
        key=lambda t: t[0],
        reverse=True,
    )


def _boundary_chars(result: AlignmentResult) -> set[str]:
    out: set[str] = set()
    for side in (result.corpus.script_a, result.corpus.script_b):
        if side.boundary_start is not None:
            out.add(side.boundary_start)
        if side.boundary_end is not None:
            out.add(side.boundary_end)
    return out


def format_correspondence_summary(
    result: AlignmentResult,
    *,
    top: int = 10,
    label: str | None = None,
    iterations: int | None = None,
    output_dir: str | Path | None = None,
    include_boundaries: bool = False,
) -> str:
    """Render the multi-line stdout block used by the example CLIs.

    The first line, when ``label`` is supplied, reads e.g.
    ``"coptic-arabic: 187 words × 10 iterations → output/"``. Then a table
    of ``top`` strongest correspondences. ``top=0`` shows every pair.
    Boundary anchors (always perfectly self-correlated) are filtered by
    default — pass ``include_boundaries=True`` to keep them.
    """
    skip = set() if include_boundaries else _boundary_chars(result)
    pairs = [
        triple
        for triple in rank_correspondences(
            result.phi, result.corpus.alphabet_a, result.corpus.alphabet_b
        )
        if triple[1] not in skip and triple[2] not in skip
    ]
    if top > 0:
        pairs = pairs[:top]

    lines: list[str] = []
    if label is not None:
        header = f"{label}: {result.corpus.n_words} words"
        if iterations is not None:
            header += f" × {iterations} iterations"
        if output_dir is not None:
            header += f" → {output_dir}"
        lines.append(header)
        lines.append("")

    heading = "All correspondences:" if top == 0 else f"Top {len(pairs)} correspondences:"
    lines.append(heading)
    for value, a, b in pairs:
        lines.append(f"  {a} ↔ {b}   φ = {value:+.3f}")
    return "\n".join(lines)


def format_phi_table(
    phi: np.ndarray,
    alphabet_a: Sequence[str],
    alphabet_b: Sequence[str],
    *,
    scale: float = 1.0,
) -> str:
    """Render φ as a tab-separated table with column headers (alphabet_b) and
    row headers (alphabet_a). Useful for pasting into a spreadsheet."""
    header = "\t" + "\t".join(alphabet_b)
    rows = [
        alphabet_a[i] + "\t" + "\t".join(f"{phi[i, j] * scale:f}" for j in range(phi.shape[1]))
        for i in range(phi.shape[0])
    ]
    return header + "\n" + "\n".join(rows)
