from __future__ import annotations


def truncate(text: str, limit: int = 3500) -> str:
    return text if len(text) <= limit else text[:limit-1] + "…"
