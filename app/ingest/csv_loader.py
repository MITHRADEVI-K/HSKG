"""CSV feedback loader utilities.

This module provides a helper for extracting the *Feedback* column from the
`Ux_data.csv` sample (or any similarly-structured CSV). We intentionally rely
only on the Python standard library to avoid adding a heavy pandas dependency.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List

__all__ = ["load_feedback_from_csv"]


def load_feedback_from_csv(
    path: str,
    text_column: str = "Feedback",
    *,
    delimiter: str | None = None,
) -> List[str]:
    """Return all non-empty values from the specified text column.

    Args:
        path: Path to the CSV file.
        text_column: Column that contains free-text user feedback.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError: If *text_column* is missing from the header row.
    """

    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"CSV not found: {path}")

    feedback: list[str] = []
    with file_path.open(newline="", encoding="utf-8", errors="ignore") as fp:
        # ------------------------------------------------------------------
        # Dialect / delimiter detection
        # ------------------------------------------------------------------
        if delimiter is None:
            sample = fp.read(4096)
            fp.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
            except csv.Error:
                dialect = csv.get_dialect("excel")  # default (comma)
            reader = csv.DictReader(fp, dialect=dialect)  # type: ignore[arg-type]
        else:
            reader = csv.DictReader(fp, delimiter=delimiter)

        # ------------------------------------------------------------------
        # Basic validation
        # ------------------------------------------------------------------
        if not reader.fieldnames or text_column not in reader.fieldnames:
            raise ValueError(
                f"Column '{text_column}' not found in {path}; "
                f"available columns: {reader.fieldnames}",
            )

        for row in reader:
            text = (row.get(text_column) or "").strip()
            if text:
                feedback.append(text)

    return feedback
