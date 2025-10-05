"""Flask blueprint exposing HSKG inference endpoints."""

from __future__ import annotations

from typing import List

from flask import Blueprint, jsonify, request

from .models.embedding import SentenceEmbedder
from .graph.builder import HSKGBuilder

hskg_bp = Blueprint("hskg", __name__, url_prefix="/api")

# Instantiate once per process (simple; for production use a proper lifecycle)
_embedder = SentenceEmbedder()
_builder = HSKGBuilder()


@hskg_bp.route("/analyze", methods=["POST"])
def analyze_text():
    """Return embedding vector for supplied text(s). Accepts JSON payload:

    {
      "text": "single sentence" OR ["list", "of", "sentences"]
    }
    """
    payload = request.get_json(force=True, silent=True)
    if payload is None or "text" not in payload:
        return jsonify({"error": "Missing 'text' in JSON body"}), 400

    texts: List[str] | str = payload["text"]
    if isinstance(texts, str):
        texts = [texts]

    vectors = _embedder.encode(texts).tolist()
    return jsonify({"vectors": vectors})


@hskg_bp.route("/graph", methods=["POST"])
def build_graph():
    """Build HSKG from provided texts and optional categories.

    Expected JSON:
    {
      "text": ["sentence1", "sentence2", ...],
      "categories": ["product", "goal", ...]  # optional, same length
    }
    """
    payload = request.get_json(force=True, silent=True)
    if payload is None or "text" not in payload:
        return jsonify({"error": "Missing 'text' in JSON body"}), 400

    texts = payload["text"]
    if isinstance(texts, str):
        texts = [texts]
    categories = payload.get("categories")
    if categories and len(categories) != len(texts):
        return jsonify({"error": "'categories' length must match 'text'"}), 400

    vectors = _embedder.encode(texts)
    graph = _builder.build(texts, vectors, categories)

    # basic stats
    edge_kinds = {}
    for _u, _v, data in graph.edges(data=True):
        kind = data.get("kind", "unknown")
        edge_kinds[kind] = edge_kinds.get(kind, 0) + 1

    return jsonify({
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "edge_breakdown": edge_kinds,
    })
