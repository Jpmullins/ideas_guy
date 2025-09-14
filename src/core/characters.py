from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import get_settings


@dataclass
class CharacterCard:
    id: str
    name: str
    description: str
    system_prompt: str
    greeting: str | None = None
    avatar: str | None = None  # path or URL served by this app

    def to_public(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
        }


def _card_from_file(path: Path) -> Optional[CharacterCard]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    name = data.get("name") or path.stem
    cid = data.get("id") or path.stem
    description = data.get("description") or ""
    system_prompt = data.get("system_prompt") or ""
    greeting = data.get("greeting")
    avatar = data.get("avatar")
    # Normalize common fields from TavernAI/Character Card v2 if present
    if not system_prompt:
        # Try common alt fields
        system_prompt = data.get("system") or data.get("prompt") or ""
    if not greeting:
        greeting = data.get("first_mes") or data.get("greeting")
    return CharacterCard(
        id=str(cid),
        name=str(name),
        description=str(description),
        system_prompt=str(system_prompt),
        greeting=greeting,
        avatar=avatar,
    )


def load_characters() -> List[CharacterCard]:
    s = get_settings()
    root = Path(s.characters_dir)
    cards: List[CharacterCard] = []
    if not root.exists():
        return cards
    for p in sorted(root.glob("*.json")):
        card = _card_from_file(p)
        if card and card.system_prompt:
            cards.append(card)
    return cards


def get_character(cid: str) -> Optional[CharacterCard]:
    for c in load_characters():
        if c.id == cid:
            return c
    return None

