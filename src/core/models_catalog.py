from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ModelOption:
    id: str
    name: str
    provider: str  # 'vllm' | 'huggingface' | 'stub'
    note: str = ""

    def to_public(self) -> dict:
        return {"id": self.id, "name": self.name, "provider": self.provider, "note": self.note}


def recommended_models() -> List[ModelOption]:
    return [
        # vLLM (OpenAI-compatible). Requires running a vLLM server separately.
        ModelOption(
            id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            name="TinyLlama 1.1B Chat",
            provider="vllm",
            note="Small instruct model; good for demos",
        ),
        ModelOption(
            id="Qwen/Qwen2.5-0.5B-Instruct",
            name="Qwen2.5 0.5B Instruct",
            provider="vllm",
            note="Very small instruct model",
        ),
        # Hugging Face local CPU-friendly examples
        ModelOption(
            id="microsoft/DialoGPT-small",
            name="DialoGPT Small (HF)",
            provider="huggingface",
            note="Dialogue-ish; simple text-generation",
        ),
        ModelOption(
            id="distilgpt2",
            name="DistilGPT-2 (HF)",
            provider="huggingface",
            note="Tiny baseline",
        ),
        # Stub for tests
        ModelOption(id="stub", name="Stub Replies", provider="stub", note="Fast, deterministic"),
    ]

