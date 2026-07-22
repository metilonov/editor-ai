from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable,Callable

from editai.domain.models import Job

logger=logging.getLogger(__name__)
Handler=Callable[[Job],Awaitable[None]]


class JobQueue:
    def __init__(self,workers:int,handler:Handler)->None:
        self.queue:asyncio.Queue[Job|None]=asyncio.Queue(); self.workers=workers; self.handler=handler; self.tasks=[]; self.cancelled:set[str]=set(); self.running:set[str]=set()
    async def start(self)->None:
        if not self.tasks: self.tasks=[asyncio.create_task(self._worker(i+1)) for i in range(self.workers)]
    async def stop(self)->None:
        for _ in self.tasks: await self.queue.put(None)
        await asyncio.gather(*self.tasks,return_exceptions=True); self.tasks.clear()
    async def add(self,job:Job)->int: await self.queue.put(job); return self.queue.qsize()
    def cancel(self,job_id:str)->bool:
        if job_id in self.running: return False
        self.cancelled.add(job_id); return True
    def snapshot(self)->dict[str,int]: return {"waiting":self.queue.qsize(),"running":len(self.running),"workers":self.workers}
    async def _worker(self,number:int)->None:
        logger.info("worker %s started",number)
        while True:
            job=await self.queue.get()
            try:
                if job is None: return
                if job.id in self.cancelled: continue
                self.running.add(job.id); await self.handler(job)
            except Exception: logger.exception("worker %s failed",number)
            finally:
                if job is not None: self.running.discard(job.id)
                self.queue.task_done()
