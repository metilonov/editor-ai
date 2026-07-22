from editai.database.database import Database

class SettingsRepository:
    def __init__(self,db:Database)->None:self.db=db
    async def get(self,user_id:int,defaults):return await self.db.get_settings(user_id,defaults)
    async def save(self,user_id:int,settings):await self.db.update_settings(user_id,settings)
