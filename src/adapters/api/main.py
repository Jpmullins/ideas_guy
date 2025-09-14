from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.adapters.api.schemas import ChatRequest, ChatResponse
from src.core.config import AppInfo, get_settings
from src.core.model import HfProvider, ModelProvider, StubProvider, VllmOpenAIProvider
from src.core.prompt import build_prompt, load_system_prompt
from src.core.characters import load_characters, get_character
from src.core.models_catalog import recommended_models


def _get_provider(kind: str | None = None, model_name: str | None = None) -> ModelProvider:
    settings = get_settings()
    kind = (kind or settings.model_provider).lower()
    model = model_name or settings.hf_model_name
    if kind == "stub":
        return StubProvider()
    if kind == "huggingface":
        return HfProvider(model)
    if kind == "vllm":
        return VllmOpenAIProvider(
            base_url=settings.vllm_endpoint,
            api_key=settings.vllm_api_key,
            model=model,
        )
    raise RuntimeError(f"Unknown MODEL_PROVIDER: {settings.model_provider}")


app = FastAPI(title="Ideas Guy Chatbot", version="0.1.0")

# CORS for local web UI
if get_settings().enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def config():
    s = get_settings()
    return {
        "app": AppInfo().model_dump(),
        "model_provider": s.model_provider,
        "hf_model_name": s.hf_model_name,
        "max_new_tokens": s.max_new_tokens,
        "temperature": s.temperature,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    s = get_settings()
    provider = _get_provider(req.model_provider, req.model_name)
    # Load character card or fallback to Ideas Guy system prompt
    system_prompt = None
    if req.character_id:
        card = get_character(req.character_id)
        if card:
            system_prompt = card.system_prompt
    if not system_prompt:
        system_prompt = load_system_prompt()
    # prepend system message
    messages = [m.model_dump() for m in req.messages]
    chat_msgs = [{"role": "system", "content": system_prompt}] + messages
    try:
        # Prefer chat-aware generation
        reply = provider.generate_from_messages(
            chat_msgs,
            max_new_tokens=req.max_new_tokens or s.max_new_tokens,
            temperature=req.temperature or s.temperature,
        )
    except Exception as e:  # pragma: no cover - surfaced by FastAPI
        raise HTTPException(status_code=500, detail=str(e))
    return ChatResponse(reply=reply)


@app.get("/api/characters")
def list_characters():
    return [c.to_public() for c in load_characters()]


@app.get("/api/characters/{cid}")
def get_character_detail(cid: str):
    c = get_character(cid)
    if not c:
        raise HTTPException(status_code=404, detail="Character not found")
    return {
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "system_prompt": c.system_prompt,
        "greeting": c.greeting,
        "avatar": c.avatar,
    }


@app.get("/api/models")
def list_models():
    return [m.to_public() for m in recommended_models()]


# Serve static web UI
# Serve UI from adapters/web/static (one level up from adapters/api)
WEB_DIR = Path(__file__).resolve().parents[1] / "web" / "static"
ASSETS_DIR = Path(get_settings().assets_dir)


@app.get("/")
def index() -> HTMLResponse:
    index_file = WEB_DIR / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
    else:
        content = "<html><body><h1>Ideas Guy</h1><p>Static UI not found.</p></body></html>"
    return HTMLResponse(content)


if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

# Best-effort serve the personality image if provided
@app.get("/assets/ideas_guy.png")
def ideas_guy_image():
    p = ASSETS_DIR / "ideas_guy.png"
    if p.exists():
        return FileResponse(str(p))
    # fallback to a generated SVG badge if missing
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
        "<rect width='100%' height='100%' fill='#ffef5e'/>"
        "<text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle'"
        " font-family='sans-serif' font-size='24' fill='#222'>IDEAS GUY</text>"
        "</svg>"
    )
    return HTMLResponse(svg, media_type="image/svg+xml")
