from editai.database.database import Database

class UserRepository:
    def __init__(self,db:Database)->None:self.db=db
    async def touch(self,user_id:int,username:str|None,first_name:str|None,defaults):await self.db.upsert_user(user_id,username,first_name,defaults)
