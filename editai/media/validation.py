from __future__ import annotations

from pathlib import Path

from editai.core.config import Settings
from editai.core.errors import MediaValidationError
from editai.domain.models import MediaInfo
from editai.media.probe import probe_media


async def validate_media(path: Path, settings: Settings) -> MediaInfo:
    if not path.exists() or not path.is_file(): raise MediaValidationError("Файл не найден")
    if path.stat().st_size > settings.max_input_mb * 1024 * 1024:
        raise MediaValidationError(f"Файл больше {settings.max_input_mb} МБ")
    info = await probe_media(path)
    if info.duration <= 0: raise MediaValidationError("Не удалось определить длительность")
    if info.duration > settings.max_video_duration_min * 60:
        raise MediaValidationError(f"Видео длиннее {settings.max_video_duration_min} минут")
    if info.width < 64 or info.height < 64: raise MediaValidationError("Слишком маленькое разрешение")
    return info
