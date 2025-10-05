"""Basic NLP preprocessing helpers using spaCy and NLTK."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import List

import nltk
import spacy
from nltk.corpus import stopwords

# Ensure NLTK stopwords downloaded (noop if already present)
try:
    nltk.data.find("corpora/stopwords")
except LookupError:  # pragma: no cover
    nltk.download("stopwords")


@lru_cache(maxsize=1)
def _stop_words() -> set[str]:
    return set(stopwords.words("english"))


@lru_cache(maxsize=1)
def _nlp():
    """Load small English spaCy model (download if missing)."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:  # pragma: no cover
        from spacy.cli import download

        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")


def preprocess_text(text: str) -> str:
    """Lower-case, remove punctuation/digits/extra-spaces, drop stopwords."""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [tok for tok in text.split() if tok not in _stop_words()]
    return " ".join(tokens)


def preprocess_batch(texts: List[str]) -> List[str]:
    return [preprocess_text(t) for t in texts]
