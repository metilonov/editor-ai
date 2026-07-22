from __future__ import annotations

from pathlib import Path

from aiogram import Bot

from editai.ingestion.telegram import download_telegram
from editai.ingestion.url import download_url


async def acquire_source(bot: Bot, kind: str, value: str, target_dir: Path) -> Path:
    if kind == "url": return await download_url(value, target_dir)
    if kind in {"telegram_video","telegram_document"}: return await download_telegram(bot, value, target_dir)
    if kind == "local": return Path(value).expanduser().resolve()
    raise RuntimeError(f"Неизвестный источник: {kind}")
