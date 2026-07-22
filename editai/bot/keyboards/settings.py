from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from editai.domain.models import UserSettings


def settings_keyboard(s:UserSettings)->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Клипов: {s.clip_count}",callback_data="set:clips"),InlineKeyboardButton(text=f"Длина: {s.clip_duration}с",callback_data="set:duration")],
        [InlineKeyboardButton(text=f"Кадр: {s.vertical_mode}",callback_data="set:vertical")],
        [InlineKeyboardButton(text=f"Субтитры: {'ON' if s.subtitles else 'OFF'}",callback_data="set:subtitles"),InlineKeyboardButton(text=f"Музыка: {'ON' if s.music else 'OFF'}",callback_data="set:music")],
        [InlineKeyboardButton(text="🎨 Выбрать профиль",callback_data="set:profile")],
    ])
