from __future__ import annotations

import re
from uuid import uuid4

from aiogram import F,Router
from aiogram.types import Message

from editai.bot.helpers import default_user_settings
from editai.core.config import Settings
from editai.database.database import Database
from editai.domain.models import Job
from editai.services.queue import JobQueue

router=Router(name="media");URL_RE=re.compile(r"https?://\S+",re.I)

async def enqueue(message:Message,kind:str,value:str,db:Database,queue:JobQueue,settings:Settings)->None:
    if not message.from_user:return
    active=await db.active_count(message.from_user.id)
    if active>=settings.max_active_jobs_per_user:
        await message.answer(f"Сначала дождитесь завершения активных задач. Лимит: {settings.max_active_jobs_per_user}.");return
    user_settings=await db.get_settings(message.from_user.id,default_user_settings(settings))
    job=Job(uuid4().hex,message.from_user.id,message.chat.id,kind,value,user_settings)
    await db.create_job(job);position=await queue.add(job)
    await message.answer(f"✅ <code>{job.id[:8]}</code> добавлена. Очередь: {position}. Профиль: {user_settings.profile}.")

@router.message(F.video)
async def video(message:Message,db:Database,queue:JobQueue,settings:Settings)->None: await enqueue(message,"telegram_video",message.video.file_id,db,queue,settings)

@router.message(F.document)
async def document(message:Message,db:Database,queue:JobQueue,settings:Settings)->None:
    doc=message.document;name=(doc.file_name or "").lower();mime=(doc.mime_type or "").lower()
    if not(mime.startswith("video/") or name.endswith((".mp4",".mov",".mkv",".webm",".avi",".m4v"))):await message.answer("Документ не похож на видео.");return
    await enqueue(message,"telegram_document",doc.file_id,db,queue,settings)

@router.message(F.text.regexp(URL_RE))
async def url(message:Message,db:Database,queue:JobQueue,settings:Settings)->None:
    match=URL_RE.search(message.text or "")
    if match: await enqueue(message,"url",match.group(0),db,queue,settings)
