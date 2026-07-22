import logging
from aiogram import Router
from aiogram.types import ErrorEvent

router=Router(name="errors");logger=logging.getLogger(__name__)

@router.errors()
async def errors(event:ErrorEvent)->bool:
    logger.exception("Telegram update error",exc_info=event.exception)
    return True
