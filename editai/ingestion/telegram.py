from __future__ import annotations

from pathlib import Path

from aiogram import Bot


async def download_telegram(bot: Bot, file_id: str, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    info = await bot.get_file(file_id)
    suffix = Path(info.file_path or "source.mp4").suffix or ".mp4"
    target = target_dir / f"source{suffix}"
    await bot.download_file(info.file_path, destination=target)
    return target
