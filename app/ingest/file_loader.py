"""Local file loader utilities (placeholder)."""

from __future__ import annotations

from pathlib import Path
from typing import List


def load_text_files(paths: List[str]) -> List[str]:
    """Return list of texts from plain-text files."""
    texts: list[str] = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            try:
                texts.append(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                texts.append(path.read_text(errors="ignore"))
    return texts
