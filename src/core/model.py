from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, *, max_new_tokens: int, temperature: float) -> str:  # pragma: no cover - interface
        ...

    def generate_from_messages(
        self, messages: List[Dict[str, str]], *, max_new_tokens: int, temperature: float
    ) -> str:
        # Default: flatten to a prompt if provider has no chat template
        lines = []
        for m in messages:
            lines.append(f"{m['role'].capitalize()}: {m['content']}")
        prompt = "\n".join(lines + ["Assistant:"])
        return self.generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)


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
        self._tokenizer = None

    def _ensure_pipeline(self):
        if self._pipe is None:
            from transformers import AutoTokenizer, pipeline  # lazy import to keep tests fast

            # text-generation works with many small models; users can override via env
            self._pipe = pipeline("text-generation", model=self.model_name)
            try:
                self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            except Exception:
                self._tokenizer = None

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

    def generate_from_messages(
        self, messages: List[Dict[str, str]], *, max_new_tokens: int, temperature: float
    ) -> str:
        self._ensure_pipeline()
        # Use chat template if available
        if self._tokenizer is not None and getattr(self._tokenizer, "apply_chat_template", None):
            try:
                text = self._tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                )
                return self.generate(text, max_new_tokens=max_new_tokens, temperature=temperature)
            except Exception:
                pass
        # Fallback to base impl
        return super().generate_from_messages(
            messages, max_new_tokens=max_new_tokens, temperature=temperature
        )


class VllmOpenAIProvider(ModelProvider):
    """Uses vLLM's OpenAI-compatible server via the `openai` SDK.

    Configure with base URL and API key via env.
    """

    def __init__(self, base_url: str, api_key: Optional[str], model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "EMPTY"
        self.model = model
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            from openai import OpenAI  # lazy import

            self._client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def generate(self, prompt: str, *, max_new_tokens: int, temperature: float) -> str:
        # Wrap the prompt in a single-turn chat to keep API uniform
        messages = [{"role": "user", "content": prompt}]
        return self.generate_from_messages(
            messages, max_new_tokens=max_new_tokens, temperature=temperature
        )

    def generate_from_messages(
        self, messages: List[Dict[str, str]], *, max_new_tokens: int, temperature: float
    ) -> str:
        self._ensure_client()
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_new_tokens,
        )
        choice = resp.choices[0]
        return (choice.message.content or "").strip()
