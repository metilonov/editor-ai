from __future__ import annotations

from collections.abc import Awaitable,Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from editai.bot.helpers import default_user_settings


class UserMiddleware(BaseMiddleware):
    async def __call__(self,handler:Callable[[TelegramObject,dict[str,Any]],Awaitable[Any]],event:TelegramObject,data:dict[str,Any])->Any:
        user=data.get("event_from_user"); db=data.get("db"); settings=data.get("settings")
        if user and db and settings: await db.upsert_user(user.id,user.username,user.first_name,default_user_settings(settings))
        return await handler(event,data)
