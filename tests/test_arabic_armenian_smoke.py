"""Smoke test: the Arabic-Armenian example runs end-to-end with bundled data."""
from pathlib import Path

import numpy as np

from arabic_armenian.run import run
from arabic_armenian.corpus_config import load_corpus


def test_bundled_data_is_loadable():
    corpus = load_corpus()
    assert corpus.n_words >= 20  # 27 valid pairs after dash-row filtering


def test_pipeline_completes(tmp_path):
    result = run(output_dir=tmp_path, iterations=3)
    assert (tmp_path / "aligned_texts.pkl").exists()
    assert np.isfinite(result.phi).all()
    assert result.phi.shape[0] == len(result.corpus.alphabet_a)
    assert result.phi.shape[1] == len(result.corpus.alphabet_b)
    # After three iterations the boundary characters should be among the
    # most-correlated pairs because they always co-occur at fixed positions.
    a_start = result.corpus.alphabet_a.index("ª")
    b_start = result.corpus.alphabet_b.index("ª")
    a_end = result.corpus.alphabet_a.index("º")
    b_end = result.corpus.alphabet_b.index("º")
    assert result.phi[a_start, b_start] > 0
    assert result.phi[a_end, b_end] > 0
