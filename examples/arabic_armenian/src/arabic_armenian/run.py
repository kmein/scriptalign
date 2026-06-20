"""CLI for the Arabic-Armenian alignment example."""

from __future__ import annotations

import argparse
from pathlib import Path

from scriptalign import (
    AlignmentResult,
    iterate_alignment,
    save_matrix_csv,
    save_state,
)

from .corpus_config import default_data_path, load_corpus


def _write_outputs(result: AlignmentResult, output_dir: Path, iteration: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    save_matrix_csv(
        output_dir / f"Co-occurrences (after alignment #{iteration}).csv",
        result.counts.occurrences,
    )
    save_matrix_csv(
        output_dir / f"phi (after alignment #{iteration}).csv",
        result.phi,
    )
    save_state(output_dir / "aligned_texts.pkl", result.corpus, result.alignments)


def run(
    *,
    input_path: Path | None = None,
    output_dir: Path,
    iterations: int = 10,
    gap_scale: float = 0.5,
) -> AlignmentResult:
    corpus = load_corpus(input_path)
    result = iterate_alignment(corpus, n_iters=iterations, gap_scale=gap_scale)
    _write_outputs(result, output_dir, iteration=iterations - 1)
    return result


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="arabic-armenian",
        description=(
            "Align Arabic words against their Armenian-script transcriptions "
            "(data from kieranmeinhardt.de/language/arabic-armenian)."
        ),
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help=f"CSV with Armenian and Arabic columns (default: bundled {default_data_path().name}).",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--gap-scale", type=float, default=0.5)
    args = parser.parse_args(argv)
    run(
        input_path=args.input,
        output_dir=args.output_dir,
        iterations=args.iterations,
        gap_scale=args.gap_scale,
    )


if __name__ == "__main__":
    main()
