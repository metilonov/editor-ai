from __future__ import annotations

import shutil
from pathlib import Path


def remove_tree(path: Path) -> None:
    if path.exists(): shutil.rmtree(path, ignore_errors=True)


def human_size(size: int | float) -> str:
    value = float(size)
    for unit in ("Б","КБ","МБ","ГБ","ТБ"):
        if value < 1024 or unit == "ТБ": return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} ТБ"


def list_music(path: Path) -> list[Path]:
    allowed = {".mp3",".wav",".m4a",".aac",".ogg",".flac"}
    return sorted(p for p in path.glob("*") if p.is_file() and p.suffix.lower() in allowed)
