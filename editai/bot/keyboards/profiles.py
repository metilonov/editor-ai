from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from editai.domain.profiles import PROFILES


def profiles_keyboard(current:str)->InlineKeyboardMarkup:
    rows=[]
    for key,p in PROFILES.items(): rows.append([InlineKeyboardButton(text=("✅ " if key==current else "")+p.title,callback_data=f"profile:{key}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
