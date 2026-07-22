from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from editai.bot.keyboards.main import main_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "🎬 <b>EditAI Ultimate Free</b>\n\n"
        "Отправьте видео, документ или ссылку. Бот найдет лучшие моменты "
        "и создаст вертикальные ролики.",
        reply_markup=main_keyboard(),
    )


@router.message(Command("help"))
@router.message(F.text == "❓ Помощь")
async def help_message(message: Message) -> None:
    await message.answer(
        "<b>Как пользоваться</b>\n"
        "1. Выберите профиль и настройки.\n"
        "2. Отправьте видео или URL.\n"
        "3. Получите клипы, обложку и manifest.json.\n\n"
        "Без STT API ролики создаются без автоматических субтитров. "
        "FFmpeg обязателен."
    )


@router.message(F.text == "🎬 Отправить видео")
async def hint(message: Message) -> None:
    await message.answer("Пришлите видео, документ с видео или ссылку одним сообщением.")
