"""Quick demo: build a text-only HSKG from the bundled `Ux_data.csv`.

Run with:
    python demo_text_pipeline.py

Note: The first run may download the HuggingFace model (~90 MB).
"""
from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

import importlib.util
from pathlib import Path as _Path

# Import app/graph/builder.py without triggering the Flask dependency chain.
_builder_path = _Path(__file__).resolve().parent / "app" / "graph" / "builder.py"
_spec = importlib.util.spec_from_file_location("hskg_builder", _builder_path)
_hskg_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
assert _spec and _spec.loader  # for mypy/static checkers
_spec.loader.exec_module(_hskg_mod)  # type: ignore[assignment]
HSKGBuilder = _hskg_mod.HSKGBuilder
# Dynamically import modules below without triggering `app.__init__`.
_csv_mod = importlib.util.spec_from_file_location(
    "csv_loader",
    _Path(__file__).resolve().parent / "app" / "ingest" / "csv_loader.py",
)
_csv_loader = importlib.util.module_from_spec(_csv_mod)  # type: ignore[arg-type]
assert _csv_mod and _csv_mod.loader
_csv_mod.loader.exec_module(_csv_loader)  # type: ignore[assignment]
load_feedback_from_csv = _csv_loader.load_feedback_from_csv
_embed_mod_spec = importlib.util.spec_from_file_location(
    "embedding",
    _Path(__file__).resolve().parent / "app" / "models" / "embedding.py",
)
_embed_mod = importlib.util.module_from_spec(_embed_mod_spec)  # type: ignore[arg-type]
assert _embed_mod_spec and _embed_mod_spec.loader
_embed_mod_spec.loader.exec_module(_embed_mod)  # type: ignore[assignment]
SentenceEmbedder = _embed_mod.SentenceEmbedder
_prep_spec = importlib.util.spec_from_file_location(
    "preprocess",
    _Path(__file__).resolve().parent / "app" / "nlp" / "preprocess.py",
)
_prep_mod = importlib.util.module_from_spec(_prep_spec)  # type: ignore[arg-type]
assert _prep_spec and _prep_spec.loader
_prep_spec.loader.exec_module(_prep_mod)  # type: ignore[assignment]
preprocess_batch = _prep_mod.preprocess_batch

CSV_PATH = Path(__file__).with_suffix("").parent / "Ux_data.csv"


def main() -> None:
    t0 = perf_counter()
    texts = load_feedback_from_csv(str(CSV_PATH))
    print(f"Loaded {len(texts)} feedback rows")

    texts_clean = preprocess_batch(texts)
    print("Pre-processing done")

    embedder = SentenceEmbedder()
    vectors = embedder.encode(texts_clean)
    print("Embeddings computed")

    builder = HSKGBuilder()
    graph = builder.build(texts_clean, vectors.numpy())
    elapsed = perf_counter() - t0

    stats = {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "elapsed_sec": round(elapsed, 2),
    }
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
