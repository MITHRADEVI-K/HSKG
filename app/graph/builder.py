"""Utilities to construct a Hybrid Semantic Knowledge Graph (HSKG).

This is a minimal placeholder illustrating how you might combine sentence
embeddings with a graph representation. Replace with your own logic once you
have the full data and research paper details.
"""

from __future__ import annotations

import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class HSKGBuilder:
    """Hybrid Semantic Knowledge Graph builder.

    Adds two edge layers:
      • symbolic edges – explicit relationships (same category)
      • similarity edges – cosine-similarity over embeddings
    """

    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
        self.graph: nx.Graph = nx.Graph()

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------
    def build(
        self,
        sentences: list[str],
        vectors: np.ndarray,
        categories: list[str] | None = None,
    ) -> nx.Graph:
        """Populate internal graph.

        Args:
            sentences: raw sentence strings.
            vectors: embedding matrix (n × d).
            categories: optional category label for each sentence.
        """
        self.graph.clear()
        categories = categories or [None] * len(sentences)
        for idx, (sent, cat) in enumerate(zip(sentences, categories)):
            self.graph.add_node(
                idx,
                text=sent,
                category=cat,
                embedding=vectors[idx].tolist(),  # small for demo; store as list
            )

        self._add_similarity_edges(vectors)
        self._add_symbolic_edges()
        return self.graph

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _add_similarity_edges(self, vectors: np.ndarray) -> None:
        sims = cosine_similarity(vectors)
        n = sims.shape[0]
        for i in range(n):
            for j in range(i + 1, n):
                if sims[i, j] >= self.threshold:
                    self.graph.add_edge(
                        i,
                        j,
                        kind="similarity",
                        weight=float(sims[i, j]),
                    )

    def _add_symbolic_edges(self) -> None:
        """Connect nodes sharing the same non-null category."""
        cat_groups: dict[str, list[int]] = {}
        for node, data in self.graph.nodes(data=True):
            cat = data.get("category")
            if cat:
                cat_groups.setdefault(cat, []).append(node)
        for cat, nodes in cat_groups.items():
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    self.graph.add_edge(nodes[i], nodes[j], kind="symbolic", label=cat)
