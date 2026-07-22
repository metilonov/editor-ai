from aiogram.types import KeyboardButton,ReplyKeyboardMarkup


def main_keyboard()->ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🎬 Отправить видео"),KeyboardButton(text="🎨 Профили")],[KeyboardButton(text="⚙️ Настройки"),KeyboardButton(text="📋 Мои задачи")],[KeyboardButton(text="❓ Помощь")]],resize_keyboard=True,input_field_placeholder="Видео, документ или ссылка")
