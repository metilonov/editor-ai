from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from editai.bot.helpers import default_user_settings
from editai.bot.keyboards.profiles import profiles_keyboard
from editai.bot.keyboards.settings import settings_keyboard
from editai.core.config import Settings
from editai.database.database import Database
from editai.domain.models import UserSettings
from editai.domain.profiles import get_profile

router = Router(name="settings")


async def _get(user_id: int, db: Database, settings: Settings) -> UserSettings:
    return await db.get_settings(user_id, default_user_settings(settings))


def _text(settings: UserSettings) -> str:
    return (
        "<b>Настройки</b>\n"
        f"Профиль: {get_profile(settings.profile).title}\n"
        f"Клипов: {settings.clip_count}\n"
        f"Длительность: {settings.clip_duration} сек.\n"
        f"Вертикальный режим: {settings.vertical_mode}\n"
        f"Субтитры: {'да' if settings.subtitles else 'нет'}\n"
        f"Музыка: {'да' if settings.music else 'нет'}"
    )


@router.message(Command("settings"))
@router.message(F.text == "⚙️ Настройки")
async def show(message: Message, db: Database, settings: Settings) -> None:
    if not message.from_user:
        return
    user_settings = await _get(message.from_user.id, db, settings)
    await message.answer(_text(user_settings), reply_markup=settings_keyboard(user_settings))


@router.message(Command("profiles"))
@router.message(F.text == "🎨 Профили")
async def profiles(message: Message, db: Database, settings: Settings) -> None:
    if not message.from_user:
        return
    user_settings = await _get(message.from_user.id, db, settings)
    await message.answer(
        "Выберите стиль монтажа:", reply_markup=profiles_keyboard(user_settings.profile)
    )


@router.callback_query(F.data.startswith("profile:"))
async def set_profile(call: CallbackQuery, db: Database, settings: Settings) -> None:
    key = (call.data or "").split(":", 1)[1]
    user_settings = await _get(call.from_user.id, db, settings)
    user_settings.profile = key
    await db.update_settings(call.from_user.id, user_settings)
    if call.message:
        await call.message.edit_text(
            f"Выбран профиль: {get_profile(key).title}",
            reply_markup=profiles_keyboard(key),
        )
    await call.answer()


@router.callback_query(F.data == "set:profile")
async def open_profiles(call: CallbackQuery, db: Database, settings: Settings) -> None:
    user_settings = await _get(call.from_user.id, db, settings)
    if call.message:
        await call.message.answer(
            "Выберите профиль:", reply_markup=profiles_keyboard(user_settings.profile)
        )
    await call.answer()


@router.callback_query(F.data.startswith("set:"))
async def cycle(call: CallbackQuery, db: Database, settings: Settings) -> None:
    user_settings = await _get(call.from_user.id, db, settings)
    key = (call.data or "").split(":", 1)[1]
    if key == "clips":
        user_settings.clip_count = 1 if user_settings.clip_count >= 5 else user_settings.clip_count + 1
    elif key == "duration":
        user_settings.clip_duration = {15: 20, 20: 30, 30: 45, 45: 60, 60: 15}.get(
            user_settings.clip_duration, 30
        )
    elif key == "vertical":
        user_settings.vertical_mode = {"blur": "crop", "crop": "fit", "fit": "blur"}.get(
            user_settings.vertical_mode, "blur"
        )
    elif key == "subtitles":
        user_settings.subtitles = not user_settings.subtitles
    elif key == "music":
        user_settings.music = not user_settings.music
    await db.update_settings(call.from_user.id, user_settings)
    if call.message:
        await call.message.edit_text(
            _text(user_settings), reply_markup=settings_keyboard(user_settings)
        )
    await call.answer("Сохранено")
