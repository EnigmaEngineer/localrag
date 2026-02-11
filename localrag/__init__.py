"""
LocalRAG — Privacy-first document intelligence.

Your data never leaves your machine unless you explicitly choose cloud mode.
"""

__version__ = "0.1.0"

from localrag.config import Settings
from localrag.core import LocalRAG

__all__ = ["LocalRAG", "Settings", "__version__"]
