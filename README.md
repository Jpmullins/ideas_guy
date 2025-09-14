# Ideas Guy Chatbot

Satirical “Ideas Guy” personality chatbot with FastAPI (OpenAPI), Hugging Face model support, and a playful web UI.

## Quick Start
- Copy `.env.example` to `.env` and adjust if needed.
- Install: `make setup`
- (Optional) Install PyTorch CPU: `source .venv/bin/activate && pip install torch --index-url https://download.pytorch.org/whl/cpu`
- Run dev server: `make dev` → http://localhost:8000
  - API docs: `/docs` and `/openapi.json`
  - Web UI: `/`

## Switching Models
Set `HF_MODEL_NAME` in `.env` (e.g., `microsoft/DialoGPT-small`, `distilgpt2`, or a fine-tuned chat model). For tests or lightweight runs, use `MODEL_PROVIDER=stub`.

## Project Layout
- `src/persona/ideas_guy.system.md` — persona prompt
- `src/core/*` — config, prompt building, model providers
- `src/adapters/api/*` — FastAPI app and schemas
- `src/adapters/web/static/*` — UI assets
- `assets/ideas_guy.png` — place persona image here (optional)
- `tests/*` — basic health and chat tests (stub)

Refer to `AGENTS.md` for contributor guidelines.

