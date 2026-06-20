import numpy as np

from scriptalign import (
    Orthography,
    build_corpus,
    format_correspondence_summary,
    iterate_alignment,
    rank_correspondences,
)


def test_rank_correspondences_returns_every_pair_sorted():
    phi = np.array([[0.1, 0.9], [-0.3, 0.5]])
    ranked = rank_correspondences(phi, ["A", "B"], ["x", "y"])
    assert len(ranked) == 4
    values = [t[0] for t in ranked]
    assert values == sorted(values, reverse=True)
    assert ranked[0] == (0.9, "A", "y")
    assert ranked[-1] == (-0.3, "B", "x")


def test_correspondence_summary_omits_boundary_anchors_by_default():
    a = Orthography(name="A", boundary_start="^", boundary_end="$")
    b = Orthography(name="B", boundary_start="^", boundary_end="$")
    corpus = build_corpus(["AB"], ["xy"], script_a=a, script_b=b)
    result = iterate_alignment(corpus, n_iters=2)
    text = format_correspondence_summary(result, top=10)
    # Boundary self-pairs ^↔^ and $↔$ would always top the list, so the
    # summary must filter them.
    assert "^ ↔ ^" not in text
    assert "$ ↔ $" not in text


def test_correspondence_summary_header_includes_label_and_output_dir():
    a = b = Orthography(name="x")
    corpus = build_corpus(["AB", "BA"], ["xy", "yx"], script_a=a, script_b=b)
    result = iterate_alignment(corpus, n_iters=1)
    text = format_correspondence_summary(
        result,
        top=3,
        label="my-cli",
        iterations=1,
        output_dir="some/dir",
    )
    assert text.startswith("my-cli: 2 words × 1 iterations → some/dir")
    assert "Top" in text


def test_correspondence_summary_show_all_when_top_zero():
    a = b = Orthography(name="x")
    corpus = build_corpus(["AB"], ["xy"], script_a=a, script_b=b)
    result = iterate_alignment(corpus, n_iters=1)
    text = format_correspondence_summary(result, top=0)
    assert "All correspondences:" in text
