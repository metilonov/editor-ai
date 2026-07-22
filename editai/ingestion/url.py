from __future__ import annotations

import asyncio
from pathlib import Path

from editai.core.errors import DownloadError


def _download_sync(url: str, target_dir: Path) -> Path:
    try: import yt_dlp
    except ImportError as exc: raise DownloadError("Не установлен yt-dlp") from exc
    target_dir.mkdir(parents=True, exist_ok=True)
    opts = {
        "outtmpl": str(target_dir / "source.%(ext)s"), "format": "bv*+ba/b", "merge_output_format": "mp4",
        "noplaylist": True, "quiet": True, "no_warnings": True,
        "postprocessors": [{"key":"FFmpegVideoRemuxer","preferedformat":"mp4"}],
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            prepared = Path(ydl.prepare_filename(info))
    except Exception as exc: raise DownloadError(f"Не удалось загрузить URL: {exc}") from exc
    candidates = sorted(target_dir.glob("source.*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates: raise DownloadError("Загрузчик не создал видеофайл")
    return next((p for p in candidates if p.suffix.lower()==".mp4"), candidates[0])


async def download_url(url: str, target_dir: Path) -> Path:
    return await asyncio.to_thread(_download_sync, url, target_dir)
