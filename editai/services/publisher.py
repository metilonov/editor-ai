from __future__ import annotations

from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile


async def publish_to_channel(bot:Bot,channel_id:int|None,files:list[Path],enabled:bool)->None:
    if not enabled or not channel_id: return
    for path in files: await bot.send_video(channel_id,FSInputFile(path),caption="🎬 EditAI",supports_streaming=True)
