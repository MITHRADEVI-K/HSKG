from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Placeholders import existing modules when available
# from .adapters import ...

app = FastAPI(title="HSKG API", version="0.1.0")
router = APIRouter(prefix="/api", tags=["HSKG"])


class IngestRequest(BaseModel):
    source_type: str
    uri: str
    options: Optional[Dict[str, Any]] = None


class NLPRequest(BaseModel):
    text: str
    language: Optional[str] = "en"
    options: Optional[Dict[str, Any]] = None


class ConceptsRequest(BaseModel):
    text: str
    domain: Optional[str] = None


class EmbedRequest(BaseModel):
    items: List[str]
    model: Optional[str] = None


class GraphBuildRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    options: Optional[Dict[str, Any]] = None


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 10


@app.get("/health", tags=["Health"])  # separate tag so /docs groups nicely
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/ingest")
async def ingest(req: IngestRequest) -> Dict[str, Any]:
    # TODO: wire to app.ingest module
    # Placeholder response structure
    return {
        "source_type": req.source_type,
        "uri": req.uri,
        "items": [],
        "message": "Ingestion started (template)",
    }


@router.post("/nlp")
async def nlp_process(req: NLPRequest) -> Dict[str, Any]:
    # TODO: wire to app.nlp pipeline
    return {
        "language": req.language,
        "tokens": [],
        "sentences": [],
        "message": "NLP processing complete (template)",
    }


@router.post("/concepts")
async def extract_concepts(req: ConceptsRequest) -> Dict[str, Any]:
    # TODO: wire to concept extraction module
    return {
        "concepts": [],
        "message": "Concept extraction complete (template)",
    }


@router.post("/embed")
async def embed(req: EmbedRequest) -> Dict[str, Any]:
    # TODO: wire to sentence-transformers or existing embedding module
    return {
        "model": req.model or "default",
        "vectors": [[0.0] * 3 for _ in req.items],
        "message": "Embedding complete (template)",
    }


@router.post("/graph")
async def build_graph(req: GraphBuildRequest) -> Dict[str, Any]:
    # TODO: wire to app.graph builder
    return {
        "nodes_count": len(req.nodes),
        "edges_count": len(req.edges),
        "message": "Graph build requested (template)",
    }


@router.post("/query")
async def query(req: QueryRequest) -> Dict[str, Any]:
    # TODO: wire to graph/vector search
    return {
        "query": req.query,
        "results": [],
        "message": "Query executed (template)",
    }


app.include_router(router)

# Optional: if running via `python -m app.api_endpoints`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.api_endpoints:app", host="0.0.0.0", port=8000, reload=True)
