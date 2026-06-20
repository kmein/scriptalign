# Coptic-Arabic Alignment

This repository ships two things:

1. **`scriptalign`** — a domain-neutral Python library for discovering letter-level correspondences between two parallel orthographies via iterative φ-coefficient scoring and Needleman-Wunsch-style alignment.
2. **`coptic-arabic`** — the original Casey alignment of Coptic-Arabic parallel text, now expressed as a client of `scriptalign`.

The main purpose of sharing it here is to demonstrate that the computational alignment operates without interference and produces the results shown in my papers. The alignment and the evidence lead; analysis comes after. All results should be confirmed by repeating the analysis.

## Install

The repo ships two Python distributions: `scriptalign` (the library) at the root, and `coptic-arabic` (the example client) under `examples/coptic_arabic/`. Install whichever you need:

```
pip install -e .                          # library only
pip install -e . -e examples/coptic_arabic   # library + example CLI
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
.venv/bin/pip install -e . -e examples/coptic_arabic
.venv/bin/python -m pytest -q
```

## Run the Coptic-Arabic alignment

```
coptic-arabic --input parallel_texts.csv --output-dir output/ --iterations 10
```

Outputs:

- `output/phi (after alignment #<i>).csv` — final φ matrix
- `output/Co-occurrences (after alignment #<i>).csv` — aligned co-occurrence counts
- `output/aligned_texts.pkl` — pickled `{words_a, words_b, alignments}`

Pass `--clipboard` to also copy a formatted φ table to the system clipboard (requires `pip install -e .[clipboard]`).

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

## Results

Viewable results in a formatted Excel spreadsheet are in [`Coptic-Arabic Text Alignment Results.xlsx`](Coptic-Arabic%20Text%20Alignment%20Results.xlsx).

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
output/                            historical run outputs (preserved)
```
