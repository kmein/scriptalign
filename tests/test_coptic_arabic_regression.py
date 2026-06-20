"""End-to-end regression for the example client.

Confirms the library reproduces the legacy align_scripts.py output bit-for-bit
when run on parallel_texts.csv for 10 iterations. The golden snapshot in
tests/data/phi_golden.npy was captured from a clean-state run of the legacy
code (see git log) and cross-checked against the committed
'output/ⲫ (after alignment #9.csv' artifact within 2e-18.
"""
from pathlib import Path

import numpy as np

from coptic_arabic.run import run

REPO_ROOT = Path(__file__).parent.parent
GOLDEN_PHI = Path(__file__).parent / "data" / "phi_golden.npy"
GOLDEN_OCCURRENCES = Path(__file__).parent / "data" / "occurrences_golden.npy"


def test_phi_matches_legacy_snapshot(tmp_path):
    result = run(
        input_path=REPO_ROOT / "parallel_texts.csv",
        output_dir=tmp_path,
        iterations=10,
    )
    expected_phi = np.load(GOLDEN_PHI)
    expected_occ = np.load(GOLDEN_OCCURRENCES)

    assert result.phi.shape == expected_phi.shape
    assert np.allclose(result.phi, expected_phi, atol=1e-12)
    assert np.allclose(result.counts.occurrences, expected_occ, atol=1e-12)


def test_outputs_are_written(tmp_path):
    run(
        input_path=REPO_ROOT / "parallel_texts.csv",
        output_dir=tmp_path,
        iterations=2,  # quick smoke
    )
    assert (tmp_path / "state.pkl").exists()
    assert (tmp_path / "phi.csv").exists()
    assert (tmp_path / "occurrences.csv").exists()
    assert (tmp_path / "correspondences.csv").exists()
    assert (tmp_path / "correspondences_ranked.tsv").exists()


def test_correspondences_ranked_is_sorted(tmp_path):
    run(
        input_path=REPO_ROOT / "parallel_texts.csv",
        output_dir=tmp_path,
        iterations=2,
    )
    lines = (tmp_path / "correspondences_ranked.tsv").read_text().splitlines()
    assert lines[0] == "a\tb\tphi"
    values = [float(line.rsplit("\t", 1)[1]) for line in lines[1:]]
    assert values == sorted(values, reverse=True)


def test_write_false_skips_disk_writes(tmp_path):
    run(
        input_path=REPO_ROOT / "parallel_texts.csv",
        output_dir=tmp_path,
        iterations=2,
        write=False,
    )
    assert not any(tmp_path.iterdir())
