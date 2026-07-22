from __future__ import annotations

import re
from pathlib import Path


def safe_filename(name: str, fallback: str = "video.mp4") -> str:
    clean = re.sub(r"[^\w.() -]+", "_", Path(name).name, flags=re.UNICODE).strip(" ._")
    return clean[:120] or fallback


def mask_secret(value: str | None) -> str:
    if not value: return "not set"
    if len(value) <= 8: return "***"
    return f"{value[:4]}…{value[-4:]}"
