from editai.database.database import Database

class JobRepository:
    def __init__(self,db:Database)->None:self.db=db
    async def add(self,job):await self.db.create_job(job)
    async def recent(self,user_id:int,limit:int=10):return await self.db.recent_jobs(user_id,limit)
