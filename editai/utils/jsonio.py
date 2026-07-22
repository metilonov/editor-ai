from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


def _default(value: Any) -> Any:
    if is_dataclass(value): return asdict(value)
    if isinstance(value, Path): return str(value)
    if hasattr(value, "value"): return value.value
    raise TypeError(type(value).__name__)


def dump_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default), encoding="utf-8")
    return path
