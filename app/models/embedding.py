from dataclasses import dataclass
from typing import List

import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer


@dataclass
class EmbeddingConfig:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


class SentenceEmbedder:
    """Utility wrapper around HuggingFace Transformer encoder."""

    def __init__(self, config: EmbeddingConfig = EmbeddingConfig()):
        self.cfg = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.cfg.model_name)
        self.model: nn.Module = AutoModel.from_pretrained(self.cfg.model_name).to(
            self.cfg.device,
        )

    @torch.inference_mode()
    def encode(self, texts: List[str]) -> torch.Tensor:
        """Return sentence embeddings for a list of texts."""
        batch = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt",
        ).to(self.cfg.device)
        outputs = self.model(**batch, return_dict=True)
        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.cpu()
