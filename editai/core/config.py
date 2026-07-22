from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from editai.core.errors import ConfigurationError

load_dotenv()


def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    return int(raw) if raw else default


def env_ids(name: str) -> frozenset[int]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return frozenset()
    try:
        return frozenset(int(item.strip()) for item in raw.split(",") if item.strip())
    except ValueError as exc:
        raise ConfigurationError(f"{name} должен содержать числовые Telegram ID") from exc


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    admin_ids: frozenset[int]
    output_channel_id: int | None
    data_dir: Path
    workers: int
    log_level: str
    max_input_mb: int
    max_video_duration_min: int
    max_active_jobs_per_user: int
    cleanup_after_hours: int
    default_profile: str
    default_clip_count: int
    default_clip_duration: int
    default_vertical_mode: str
    default_subtitles: bool
    default_music: bool
    transcription_api_url: str | None
    transcription_api_key: str | None
    transcription_model: str
    transcription_language: str
    publish_to_channel: bool
    keep_source_files: bool
    keep_analysis_files: bool
    keep_temp_files: bool

    @property
    def input_dir(self) -> Path: return self.data_dir / "input"
    @property
    def output_dir(self) -> Path: return self.data_dir / "output"
    @property
    def temp_dir(self) -> Path: return self.data_dir / "temp"
    @property
    def logs_dir(self) -> Path: return self.data_dir / "logs"
    @property
    def db_path(self) -> Path: return self.data_dir / "editai.db"

    def ensure_dirs(self) -> None:
        for path in (self.data_dir, self.input_dir, self.output_dir, self.temp_dir, self.logs_dir):
            path.mkdir(parents=True, exist_ok=True)


def load_settings(require_token: bool = True) -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if require_token and (not token or token.endswith("CHANGE_ME")):
        raise ConfigurationError("Укажите BOT_TOKEN в .env")
    output_channel = os.getenv("OUTPUT_CHANNEL_ID", "").strip()
    settings = Settings(
        bot_token=token,
        admin_ids=env_ids("ADMIN_IDS"),
        output_channel_id=int(output_channel) if output_channel else None,
        data_dir=Path(os.getenv("DATA_DIR", "data")).expanduser().resolve(),
        workers=max(1, min(env_int("WORKERS", 1), 4)),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        max_input_mb=max(20, env_int("MAX_INPUT_MB", 500)),
        max_video_duration_min=max(1, env_int("MAX_VIDEO_DURATION_MIN", 180)),
        max_active_jobs_per_user=max(1, env_int("MAX_ACTIVE_JOBS_PER_USER", 2)),
        cleanup_after_hours=max(1, env_int("CLEANUP_AFTER_HOURS", 24)),
        default_profile=os.getenv("DEFAULT_PROFILE", "dynamic").strip().lower(),
        default_clip_count=max(1, min(env_int("DEFAULT_CLIP_COUNT", 3), 10)),
        default_clip_duration=max(10, min(env_int("DEFAULT_CLIP_DURATION", 30), 60)),
        default_vertical_mode=os.getenv("DEFAULT_VERTICAL_MODE", "blur").strip().lower(),
        default_subtitles=env_bool("DEFAULT_SUBTITLES"),
        default_music=env_bool("DEFAULT_MUSIC"),
        transcription_api_url=os.getenv("TRANSCRIPTION_API_URL", "").strip() or None,
        transcription_api_key=os.getenv("TRANSCRIPTION_API_KEY", "").strip() or None,
        transcription_model=os.getenv("TRANSCRIPTION_MODEL", "whisper-large-v3").strip(),
        transcription_language=os.getenv("TRANSCRIPTION_LANGUAGE", "ru").strip(),
        publish_to_channel=env_bool("PUBLISH_TO_CHANNEL"),
        keep_source_files=env_bool("KEEP_SOURCE_FILES"),
        keep_analysis_files=env_bool("KEEP_ANALYSIS_FILES", True),
        keep_temp_files=env_bool("KEEP_TEMP_FILES"),
    )
    settings.ensure_dirs()
    return settings
