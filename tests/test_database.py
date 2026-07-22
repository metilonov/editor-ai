import pytest
from editai.database.database import Database
from editai.domain.models import UserSettings

@pytest.mark.asyncio
async def test_database(tmp_path):
    db=Database(tmp_path/"db.sqlite");await db.init();s=UserSettings();await db.upsert_user(1,"u","n",s)
    got=await db.get_settings(1,s);assert got.profile=="dynamic"
