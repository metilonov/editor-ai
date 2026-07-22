from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from editai.database.database import Database
from editai.domain.enums import JobStatus
from editai.services.queue import JobQueue

router = Router(name="jobs")


@router.message(Command("jobs"))
@router.message(F.text == "📋 Мои задачи")
async def jobs(message: Message, db: Database) -> None:
    if not message.from_user:
        return
    rows = await db.recent_jobs(message.from_user.id, 10)
    if not rows:
        await message.answer("Задач пока нет.")
        return
    icons = {
        "queued": "⏳", "downloading": "⬇️", "validating": "🧪",
        "analyzing": "🔍", "transcribing": "💬", "rendering": "🎞",
        "sending": "📤", "completed": "✅", "failed": "❌", "cancelled": "🚫",
    }
    lines = ["<b>Последние задачи</b>"]
    for row in rows:
        created = datetime.fromtimestamp(float(row["created_at"])).strftime("%d.%m %H:%M")
        lines.append(
            f"<code>{row['id'][:8]}</code> · {created} · "
            f"{icons.get(row['status'], '')} {row['status']} · файлов: {row['output_count']}"
        )
    lines.append("\nОтмена ожидающей: <code>/cancel ID</code>")
    await message.answer("\n".join(lines))


@router.message(Command("cancel"))
async def cancel(
    message: Message, command: CommandObject, db: Database, queue: JobQueue
) -> None:
    if not message.from_user:
        return
    prefix = (command.args or "").strip()
    if not prefix:
        await message.answer("Пример: /cancel a1b2c3d4")
        return
    job_id = await db.resolve_prefix(message.from_user.id, prefix)
    if not job_id:
        await message.answer("Ожидающая задача с таким ID не найдена или ID неоднозначен.")
        return
    if not queue.cancel(job_id):
        await message.answer("Задача уже обрабатывается и не может быть безопасно отменена.")
        return
    await db.set_status(job_id, JobStatus.CANCELLED)
    await message.answer("🚫 Отменено.")
