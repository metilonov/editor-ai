from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from editai.core.config import Settings
from editai.database.database import Database
from editai.services.cleanup import cleanup_old
from editai.services.health import health_snapshot
from editai.services.queue import JobQueue

router = Router(name="admin")


def allowed(message: Message, settings: Settings) -> bool:
    return bool(message.from_user and message.from_user.id in settings.admin_ids)


@router.message(Command("stats"))
async def stats(
    message: Message, settings: Settings, db: Database, queue: JobQueue
) -> None:
    if not allowed(message, settings):
        return
    data = await db.statistics()
    queue_data = queue.snapshot()
    await message.answer(
        "<b>Статистика</b>\n"
        f"Пользователи: {data['users']}\n"
        f"Задачи: {data['jobs']}\n"
        f"Активные: {data['active']}\n"
        f"Завершено: {data['completed']}\n"
        f"Ошибки: {data['failed']}\n"
        f"Очередь: {queue_data['waiting']}\n"
        f"Worker: {queue_data['workers']}"
    )


@router.message(Command("health"))
async def health(message: Message, settings: Settings) -> None:
    if not allowed(message, settings):
        return
    data = health_snapshot(settings.data_dir)
    await message.answer(
        "<b>Health</b>\n" + "\n".join(f"{key}: {value}" for key, value in data.items())
    )


@router.message(Command("cleanup"))
async def cleanup(message: Message, settings: Settings) -> None:
    if not allowed(message, settings):
        return
    count = await cleanup_old(settings.temp_dir, settings.cleanup_after_hours)
    await message.answer(f"Удалено объектов: {count}")
