from __future__ import annotations

import shutil
from pathlib import Path

from editai.media.process import run_process


def ensure_ffmpeg() -> None:
    missing = [name for name in ("ffmpeg","ffprobe") if not shutil.which(name)]
    if missing: raise RuntimeError("Не найдены: " + ", ".join(missing))


async def extract_audio(source: Path, target: Path, rate: int = 16000) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    await run_process("ffmpeg","-y","-i",str(source),"-vn","-ac","1","-ar",str(rate),"-c:a","pcm_s16le",str(target),timeout=1800)
    return target


async def make_thumbnail(source: Path, timestamp: float, target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    await run_process("ffmpeg","-y","-ss",f"{timestamp:.3f}","-i",str(source),"-frames:v","1","-vf","scale=720:-2",str(target),timeout=180)
    return target
