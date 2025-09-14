from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, *, max_new_tokens: int, temperature: float) -> str:  # pragma: no cover - interface
        ...


class StubProvider(ModelProvider):
    def generate(self, prompt: str, *, max_new_tokens: int, temperature: float) -> str:
        return (
            "Okay, picture this: a fridge that tweets your leftovers, "
            "a subscription for socks that never match, and an app that rates your ideas "
            "before you pitch them. Boom."
        )


class HfProvider(ModelProvider):
    def __init__(self, model_name: str = "distilgpt2") -> None:
        self.model_name = model_name
        self._pipe = None  # lazy init

    def _ensure_pipeline(self):
        if self._pipe is None:
            from transformers import pipeline  # lazy import to keep tests fast

            # text-generation works with many small models; users can override via env
            self._pipe = pipeline("text-generation", model=self.model_name)

    def generate(self, prompt: str, *, max_new_tokens: int, temperature: float) -> str:
        self._ensure_pipeline()
        outputs = self._pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            return_full_text=False,
        )
        text: str = outputs[0]["generated_text"]
        return text.strip()

