"""Arabic-Armenian letter alignment — example client of the scriptalign library.

Data source: https://kieranmeinhardt.de/language/arabic-armenian/
"""

from .orthographies import ARABIC, ARMENIAN
from .corpus_config import default_data_path, load_corpus

__all__ = ["ARABIC", "ARMENIAN", "default_data_path", "load_corpus"]
