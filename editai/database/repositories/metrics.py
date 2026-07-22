from editai.database.database import Database

class MetricsRepository:
    def __init__(self,db:Database)->None:self.db=db
    async def snapshot(self):return await self.db.statistics()
