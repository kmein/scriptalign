# Coptic-Arabic Alignment

This repository ships two things:

1. **`scriptalign`** — a domain-neutral Python library for discovering letter-level correspondences between two parallel orthographies via iterative φ-coefficient scoring and Needleman-Wunsch-style alignment.
2. **`coptic-arabic`** — the original Casey alignment of Coptic-Arabic parallel text, now expressed as a client of `scriptalign`.

The main purpose of sharing it here is to demonstrate that the computational alignment operates without interference and produces the results shown in my papers. The alignment and the evidence lead; analysis comes after. All results should be confirmed by repeating the analysis.

## Install

The repo ships three Python distributions: `scriptalign` (the library) at the root, and two example clients under `examples/`. Install whichever you need:

```
pip install -e .                                                       # library only
pip install -e . -e examples/coptic_arabic                             # + Coptic-Arabic CLI
pip install -e . -e examples/coptic_arabic -e examples/arabic_armenian # everything
```

### With Nix

A `flake.nix` builds the library and the example clients and exposes their CLIs as runnable apps:

```
nix build .#scriptalign        # library as a Python package
nix build .#coptic-arabic      # Coptic-Arabic CLI (default package)
nix build .#arabic-armenian    # Arabic-Armenian CLI

nix run  .#coptic-arabic -- --input parallel_texts.csv --output-dir output/
nix run  .#arabic-armenian -- --output-dir output-aa/    # bundled corpus

nix develop                    # dev shell: python + numpy + pytest + pyperclip
```

Inside `nix develop`, set up an editable install for development:

```
python -m venv --system-site-packages .venv
.venv/bin/pip install -e . -e examples/coptic_arabic -e examples/arabic_armenian
.venv/bin/python -m pytest -q
```

## Run the Coptic-Arabic alignment

```
coptic-arabic --input parallel_texts.csv --output-dir output/ --iterations 10
```

prints a summary to stdout:

```
coptic-arabic: 187 words × 10 iterations → output/

Top 10 correspondences:
  ϧ ↔ خ   φ = +1.000
  ϥ ↔ ف   φ = +0.983
  ⲣ ↔ ر   φ = +0.954
  ⲙ ↔ م   φ = +0.881
  ...
```

and writes to `output/`:

- `correspondences.csv` — **φ matrix with letter labels** (column headers = Arabic alphabet, row labels = Coptic alphabet). Open in a spreadsheet to inspect any pair.
- `correspondences_ranked.tsv` — one letter pair per line, sorted strongest-correlated first. Three tab-separated columns: `a`, `b`, `phi`.
- `phi.csv` — raw φ matrix, unlabeled (for code consumers).
- `occurrences.csv` — raw aligned co-occurrence counts.
- `state.pkl` — pickled `{words_a, words_b, alignments}`.

### Quick look without writing files

```
coptic-arabic --input parallel_texts.csv --show 20    # top-20 to stdout, no writes
coptic-arabic --input parallel_texts.csv --show 0     # every pair
```

### Other flags

- `--top N` — how many rows the post-run summary table includes (default 10).
- `--iterations N` — refinement iterations (default 10).
- `--gap-scale F` — DP gap penalty scale (default 0.5).
- `--clipboard` — copy a formatted φ table to the system clipboard (requires `pip install -e .[clipboard]`).

## Run the Arabic-Armenian alignment

The Arabic-Armenian example aligns Arabic philosophical terms against their Armenian-script transcriptions in a small 27-pair corpus. The data is bundled with the package, so the CLI runs with no arguments:

```
arabic-armenian --output-dir output-aa/ --iterations 10
```

prints a summary to stdout:

```
arabic-armenian: 27 words × 10 iterations → output-aa/

Top 10 correspondences:
  հ ↔ ه   φ = +1.000
  ք ↔ ك   φ = +1.000
  լ ↔ ل   φ = +0.830
  մ ↔ م   φ = +0.818
  ջ ↔ ج   φ = +0.814
  թ ↔ ة   φ = +0.794
  ր ↔ ر   φ = +0.738
  ֆ ↔ ف   φ = +0.738
  ն ↔ ن   φ = +0.700
  ...
```

and writes the same five files (`correspondences.csv`, `correspondences_ranked.tsv`, `phi.csv`, `occurrences.csv`, `state.pkl`) into `output-aa/`. All the flags from the Coptic-Arabic CLI apply (`--show N`, `--top N`, `--iterations`, `--gap-scale`); `--input` is optional and only needed to point at a CSV other than the bundled one.

Source of the corpus: <https://kieranmeinhardt.de/language/arabic-armenian/>.

## Use the library on a different pair of scripts

```python
from scriptalign import Orthography, load_parallel_corpus, iterate_alignment

source = Orthography(name="source", normalize=str.lower,
                     boundary_start="^", boundary_end="$")
target = Orthography(name="target", normalize=str.lower)

corpus = load_parallel_corpus(
    "my_pairs.csv",
    column_a="source_word",
    column_b="target_word",
    script_a=source,
    script_b=target,
)
result = iterate_alignment(corpus, n_iters=10)
# result.phi: ndarray of letter-pair correlations
# result.alignments: per-word list of (i, j) index pairs
```

The library is deliberately agnostic about which scripts you're aligning, what your CSV columns are called, and how you normalize each side. The Coptic-Arabic specifics live entirely in `examples/coptic_arabic/`.

## Data sources

Input is in `parallel_texts.csv`. These data are taken from:

* [Casanova, Paul (1901). Un texte arabe transcrit en caractères coptes. *Le Bulletin de l'Institut français d'archéologie orientale* 1:1-20.](http://www.ifao.egnet.net/bifao/1/)
* [Burmester, OHE (1965-1966). Further leaves from the Arabic MS. in Coptic script of the Apophthegmata Patrum. *Bulletin de la Société d'archéologie copte* 18:51-64.](https://copticsounds.files.wordpress.com/2010/01/furtherleavesfromthearabicmsincopticscriptoftheapophthehmatapatrum.pdf)

Additional data found in Sobhy 1926 have not yet been added. Updated readings of the Arabic found in Blau 1979 have not yet been included.

Coptic `<ⲟⲩ>` has been replaced with `<ȣ>` so that it is treated as a single grapheme by the analysis.

## Examples

The repo ships two example clients of `scriptalign`:

- **`examples/coptic_arabic/`** — letter alignment of Coptic-script Arabic against vocalized Arabic. Operates on `parallel_texts.csv` at the repo root (Casanova 1901 + Burmester 1965-66).
- **`examples/arabic_armenian/`** — letter alignment of Arabic against Armenian-script transcriptions of Arabic philosophical terminology. Data is bundled with the package; runs out of the box. Source: <https://kieranmeinhardt.de/language/arabic-armenian/>.

## Repository layout

```
src/scriptalign/                   the library — domain-neutral
examples/coptic_arabic/            example: Coptic-Arabic alignment
examples/arabic_armenian/          example: Arabic-Armenian alignment (data bundled)
tests/                             unit + regression + smoke tests
parallel_texts.csv                 Coptic-Arabic input corpus
```
