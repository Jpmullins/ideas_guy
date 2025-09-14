from pathlib import Path


def load_system_prompt(path: str | None = None) -> str:
    if not path:
        path = "src/persona/ideas_guy.system.md"
    p = Path(path)
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return (
        "You are the satirical 'Ideas Guy': overconfident, rapid-fire ideas,"
        " but ultimately helpful and safe."
    )


def build_prompt(system_prompt: str, messages: list[dict[str, str]]) -> str:
    preface = (
        f"System:\n{system_prompt}\n\n"
        "Conversation (continue as the Assistant):\n"
    )
    formatted: list[str] = []
    for m in messages:
        role = m.get("role", "user").strip()
        content = (m.get("content") or "").strip()
        if role not in {"system", "user", "assistant"}:
            role = "user"
        role_cap = "User" if role == "user" else "Assistant"
        formatted.append(f"{role_cap}: {content}")
    # Ensure the model completes the Assistant turn
    if not formatted or not formatted[-1].startswith("Assistant:"):
        formatted.append("Assistant:")
    return preface + "\n".join(formatted)

