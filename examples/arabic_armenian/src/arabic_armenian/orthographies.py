"""Armenian and Arabic orthographies used in this corpus."""

from __future__ import annotations

from scriptalign import Orthography

_ARABIC_TERMINAL_DIACRITICS = frozenset(chr(c) for c in range(0x064B, 0x0660))
_ARABIC_SUKUN = "ْ"
_ARMENIAN_DIGRAPH = "ու"  # written as two characters; phonetically /u/
_ARMENIAN_DIGRAPH_SENTINEL = "ʊ"  # private single-codepoint stand-in
_BOUNDARY_START = "ª"
_BOUNDARY_END = "º"


def _normalize_armenian(word: str) -> str:
    # Collapse the ու digraph to a single grapheme, then drop intra-word
    # spaces so multi-word phrases (rows 9 and 10) participate as one
    # sequence in the alignment.
    return word.replace(_ARMENIAN_DIGRAPH, _ARMENIAN_DIGRAPH_SENTINEL).replace(" ", "")


def _normalize_arabic(word: str) -> str:
    word = word.replace(_ARABIC_SUKUN, "").replace(" ", "")
    if word and word[-1] in _ARABIC_TERMINAL_DIACRITICS:
        word = word[:-1]
    return word


ARMENIAN = Orthography(
    name="Armenian",
    normalize=_normalize_armenian,
    boundary_start=_BOUNDARY_START,
    boundary_end=_BOUNDARY_END,
)

ARABIC = Orthography(
    name="Arabic",
    normalize=_normalize_arabic,
    boundary_start=_BOUNDARY_START,
    boundary_end=_BOUNDARY_END,
)
