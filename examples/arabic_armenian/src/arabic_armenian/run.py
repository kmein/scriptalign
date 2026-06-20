"""CLI for the Arabic-Armenian alignment example."""

from __future__ import annotations

import argparse
from pathlib import Path

from scriptalign import (
    AlignmentResult,
    format_correspondence_summary,
    iterate_alignment,
    save_correspondences_tsv,
    save_labeled_matrix_csv,
    save_matrix_csv,
    save_state,
)

from .corpus_config import default_data_path, load_corpus


def _write_outputs(result: AlignmentResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    a, b = result.corpus.alphabet_a, result.corpus.alphabet_b
    save_matrix_csv(output_dir / "phi.csv", result.phi)
    save_matrix_csv(output_dir / "occurrences.csv", result.counts.occurrences)
    save_labeled_matrix_csv(output_dir / "correspondences.csv", result.phi, a, b)
    save_correspondences_tsv(
        output_dir / "correspondences_ranked.tsv", result.phi, a, b
    )
    save_state(output_dir / "state.pkl", result.corpus, result.alignments)


def run(
    *,
    input_path: Path | None = None,
    output_dir: Path,
    iterations: int = 10,
    gap_scale: float = 0.5,
    write: bool = True,
) -> AlignmentResult:
    corpus = load_corpus(input_path)
    result = iterate_alignment(corpus, n_iters=iterations, gap_scale=gap_scale)
    if write:
        _write_outputs(result, output_dir)
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
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="How many correspondences to show in the post-run summary.",
    )
    parser.add_argument(
        "--show",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Print the top N correspondences and skip writing files. "
            "Use --show 0 to print every pair."
        ),
    )
    args = parser.parse_args(argv)

    write = args.show is None
    result = run(
        input_path=args.input,
        output_dir=args.output_dir,
        iterations=args.iterations,
        gap_scale=args.gap_scale,
        write=write,
    )

    if write:
        summary = format_correspondence_summary(
            result,
            top=args.top,
            label=parser.prog,
            iterations=args.iterations,
            output_dir=args.output_dir,
        )
    else:
        summary = format_correspondence_summary(
            result,
            top=args.show,
            label=parser.prog,
            iterations=args.iterations,
        )
    print(summary)


if __name__ == "__main__":
    main()
