# Repository Guidelines

This repo hosts a personality chat bot based on the satirical “ideas guy.” Keep changes small, well‑scoped, and consistent with the persona.

## Project Structure & Module Organization
- `src/` — bot code organized by feature:
  - `src/persona/` — prompt templates and rules (e.g., `ideas_guy.system.md`, `style_guide.md`).
  - `src/adapters/` — chat I/O (CLI, web, Discord, etc.).
  - `src/core/` — conversation loop, memory, safety filters.
- `tests/` — mirrors `src/` (e.g., `tests/persona/test_style.py`, `tests/core/conversation.spec.ts`).
- `assets/` — static assets; include `assets/ideas_guy.png` for UI/branding.
- `scripts/` — dev and CI helpers (data prep, eval, export transcripts).
- `docs/` — design notes, prompt rationale, and guardrails.

## Build, Test, and Development Commands
- `make setup` — install deps (backend and any UI).
- `make dev` — run local chat (CLI or web) with hot reload.
- `make test` — run unit/integration tests.
- `make lint` / `make fmt` — lint and auto‑format.
- `make build` — production bundle or package.
No Makefile? Use stack commands: Python `pytest -q`, `ruff check`, `black .`; JS/TS `npm test`, `eslint .`, `prettier -w .`, `npm run dev`.

## Coding Style & Naming Conventions
- Indentation: Python 4 spaces; JS/TS 2 spaces. Max line length 100.
- Names: packages/modules `lower_snake_case`; classes `PascalCase`; functions/vars `snake_case` (Py) or `camelCase` (JS/TS).
- Persona assets: system prompt `ideas_guy.system.md`; seed examples `*.seed.md`.
- Tools: Python — `black`, `ruff`; JS/TS — `prettier`, `eslint`. Fix before commit.

## Testing Guidelines
- Focus on conversational behavior: snapshot key replies and assert persona traits (confident, rapid‑fire ideas; non‑harmful).
- Structure: tests mirror `src/`. Filenames: `test_*.py` or `*.spec.ts`/`*.test.ts`.
- Determinism: seed RNG, stub network calls, and fix timestamps.
- Run `make test` (or `pytest -q` / `npm test`) before pushing.

## Commit & Pull Request Guidelines
- Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`). Reference issues (`Fixes #123`).
- PRs include: purpose, user impact, sample transcript, screenshots using `assets/ideas_guy.png`, and test notes.
- CI must pass (format, lint, tests). Update docs when prompts/persona change.

## Security & Configuration Tips
- Never commit secrets; use `.env` with `.env.example` describing keys.
- Log redaction for PII; validate inputs at adapter boundaries; review dependencies.
