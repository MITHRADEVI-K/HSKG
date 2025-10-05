"""Concept extraction and categorization using spaCy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import spacy

# Categories from research paper
UX_CATEGORIES = {"product", "setting", "state", "user"}
DESIGN_CATEGORIES = {"goal", "fix", "item"}

NLP = spacy.load("en_core_web_sm")


@dataclass
class Concept:
    text: str
    category: str | None
    start_char: int
    end_char: int


def _assign_category(token_text: str) -> str | None:
    """Very naive keyword-based category mapping. Replace with better rules."""
    lower = token_text.lower()
    if lower in UX_CATEGORIES:
        return lower
    if lower in DESIGN_CATEGORIES:
        return lower
    return None


def extract_concepts(texts: List[str]) -> List[Concept]:
    concepts: list[Concept] = []
    for doc_text in texts:
        doc = NLP(doc_text)
        for ent in doc.ents:
            category = _assign_category(ent.text)
            concepts.append(
                Concept(
                    text=ent.text,
                    category=category,
                    start_char=ent.start_char,
                    end_char=ent.end_char,
                ),
            )
    return concepts
