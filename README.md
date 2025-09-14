# Ideas Guy Chatbot

Satirical “Ideas Guy” personality chatbot with FastAPI (OpenAPI), Hugging Face model support, and a playful web UI.

## Quick Start
- Copy `.env.example` to `.env` and adjust if needed.
- Install: `make setup`
- (Optional) Install PyTorch CPU: `source .venv/bin/activate && pip install torch --index-url https://download.pytorch.org/whl/cpu`
- Run dev server: `make dev` → http://localhost:8000
  - API docs: `/docs` and `/openapi.json`
  - Web UI: `/` (pick Character and Model in the header)

## Switching Models
- vLLM (default): set `MODEL_PROVIDER=vllm` and choose an instruct/chat model in `HF_MODEL_NAME`.
  - Example (small, CPU‑friendly-ish):
    - `python -m vllm.entrypoints.openai.api_server --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --port 8001`
    - In `.env`: `VLLM_ENDPOINT=http://localhost:8001/v1` (API key optional).
- Hugging Face local: set `MODEL_PROVIDER=huggingface` and `HF_MODEL_NAME` (e.g., `microsoft/DialoGPT-small`). Install a backend like PyTorch.
- For tests or lightweight runs, use `MODEL_PROVIDER=stub`.

## Project Layout
- `src/persona/ideas_guy.system.md` — persona prompt
- `src/core/*` — config, prompt building, model providers
- `src/adapters/api/*` — FastAPI app and schemas
- `src/adapters/web/static/*` — UI assets
- `assets/ideas_guy.png` — place persona image here (optional)
- `tests/*` — basic health and chat tests (stub)
 - `characters/*.json` — Character cards (selectable in UI)

Refer to `AGENTS.md` for contributor guidelines. Character cards follow a simple JSON format with `id`, `name`, `description`, `system_prompt`, `greeting`, and `avatar`.
