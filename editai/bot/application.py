from __future__ import annotations

from contextlib import suppress

from aiogram import Bot,Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from editai.bot.handlers import build_router
from editai.bot.middlewares.user import UserMiddleware
from editai.core.config import load_settings
from editai.core.logging import configure_logging
from editai.database.database import Database
from editai.media.ffmpeg import ensure_ffmpeg
from editai.services.job_pipeline import JobProcessor
from editai.services.queue import JobQueue


async def main()->None:
    settings=load_settings();configure_logging(settings.log_level,settings.logs_dir);ensure_ffmpeg()
    bot=Bot(settings.bot_token,default=DefaultBotProperties(parse_mode=ParseMode.HTML));db=Database(settings.db_path);await db.init()
    processor=JobProcessor(bot,db,settings);queue=JobQueue(settings.workers,processor);await queue.start()
    dp=Dispatcher();router=build_router();router.message.middleware(UserMiddleware());router.callback_query.middleware(UserMiddleware());dp.include_router(router)
    dp["settings"]=settings;dp["db"]=db;dp["queue"]=queue
    try: await dp.start_polling(bot)
    finally:
        await queue.stop()
        with suppress(Exception): await bot.session.close()
