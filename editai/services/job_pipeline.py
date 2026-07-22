from __future__ import annotations

import logging
from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile

from editai.analysis.pipeline import analyze
from editai.api.transcription import TranscriptionClient
from editai.core.config import Settings
from editai.database.database import Database
from editai.domain.enums import JobStatus
from editai.domain.models import Job
from editai.editing.pipeline import render_all
from editai.ingestion.router import acquire_source
from editai.media.validation import validate_media
from editai.services.publisher import publish_to_channel
from editai.utils.files import remove_tree
from editai.utils.timecode import human_duration

logger = logging.getLogger(__name__)


class JobProcessor:
    def __init__(self, bot: Bot, db: Database, settings: Settings) -> None:
        self.bot = bot
        self.db = db
        self.settings = settings
        self.stt = TranscriptionClient(
            settings.transcription_api_url,
            settings.transcription_api_key,
            settings.transcription_model,
            settings.transcription_language,
        )

    async def __call__(self, job: Job) -> None:
        root = self.settings.temp_dir / job.id
        input_dir = root / "input"
        work_dir = root / "work"
        output_dir = self.settings.output_dir / job.id
        for path in (input_dir, work_dir, output_dir):
            path.mkdir(parents=True, exist_ok=True)
        try:
            await self.db.set_status(job.id, JobStatus.DOWNLOADING)
            await self.bot.send_message(job.chat_id, f"⬇️ <code>{job.id[:8]}</code>: загружаю…")
            source = await acquire_source(self.bot, job.source_kind, job.source_value, input_dir)

            await self.db.set_status(job.id, JobStatus.VALIDATING)
            info = await validate_media(source, self.settings)

            await self.db.set_status(job.id, JobStatus.ANALYZING)
            await self.bot.send_message(
                job.chat_id,
                f"🔍 Анализирую {human_duration(info.duration)}: "
                "сцены, движение, звук, лица и качество…",
            )
            selected, _, wav, analysis_path = await analyze(
                source,
                info,
                work_dir,
                job.settings.profile,
                job.settings.clip_duration,
                job.settings.clip_count,
            )

            subtitles = []
            if job.settings.subtitles and wav and self.stt.enabled:
                await self.db.set_status(job.id, JobStatus.TRANSCRIBING)
                await self.bot.send_message(job.chat_id, "💬 Создаю субтитры…")
                try:
                    subtitles = await self.stt.transcribe(wav)
                except Exception:
                    logger.exception("transcription failed")

            await self.db.set_status(job.id, JobStatus.RENDERING)
            await self.bot.send_message(
                job.chat_id,
                f"🎞 Рендерю {len(selected)} клипа(ов) в стиле {job.settings.profile}…",
            )
            outputs, manifest, thumb = await render_all(
                source,
                info,
                selected,
                subtitles,
                job.settings,
                output_dir,
                work_dir,
                Path("assets/music").resolve(),
            )

            await self.db.set_status(
                job.id,
                JobStatus.SENDING,
                analysis_path=analysis_path,
                manifest_path=manifest,
                output_count=len(outputs),
            )
            for index, (path, segment) in enumerate(zip(outputs, selected), 1):
                reasons = ", ".join(segment.reasons) or "общая динамика"
                caption = (
                    f"🎬 <b>Клип {index}/{len(outputs)}</b> · "
                    f"{human_duration(segment.start)}–{human_duration(segment.end)}\n"
                    f"Оценка: {segment.score * 100:.0f}/100\n"
                    f"Почему выбран: {reasons}"
                )
                try:
                    kwargs = {
                        "chat_id": job.chat_id,
                        "video": FSInputFile(path),
                        "caption": caption,
                        "supports_streaming": True,
                    }
                    if thumb:
                        kwargs["thumbnail"] = FSInputFile(thumb)
                    await self.bot.send_video(**kwargs)
                except Exception:
                    await self.bot.send_document(job.chat_id, FSInputFile(path), caption=caption)

            await self.bot.send_document(
                job.chat_id, FSInputFile(manifest), caption="JSON-манифест проекта"
            )
            await publish_to_channel(
                self.bot,
                self.settings.output_channel_id,
                outputs,
                self.settings.publish_to_channel,
            )
            await self.db.set_status(
                job.id,
                JobStatus.COMPLETED,
                analysis_path=analysis_path,
                manifest_path=manifest,
                output_count=len(outputs),
            )
            await self.bot.send_message(job.chat_id, "✅ Обработка завершена.")
        except Exception as exc:
            logger.exception("job %s failed", job.id)
            await self.db.set_status(job.id, JobStatus.FAILED, error=str(exc)[:1000])
            try:
                await self.bot.send_message(
                    job.chat_id,
                    f"❌ Ошибка <code>{job.id[:8]}</code>: {str(exc)[:700]}",
                )
            except Exception:
                pass
        finally:
            if not self.settings.keep_temp_files:
                remove_tree(root)
