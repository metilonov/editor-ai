from __future__ import annotations

import asyncio
import json
import sqlite3
from pathlib import Path
from time import time
from typing import Any

from editai.database.schema import SCHEMA
from editai.domain.enums import JobStatus
from editai.domain.models import Job,UserSettings


class Database:
    def __init__(self,path:Path)->None: self.path=path; self._lock=asyncio.Lock()
    def _connect(self)->sqlite3.Connection:
        conn=sqlite3.connect(self.path); conn.row_factory=sqlite3.Row; return conn
    async def init(self)->None: await asyncio.to_thread(self._init)
    def _init(self)->None:
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self._connect() as conn: conn.executescript(SCHEMA)
    async def upsert_user(self,user_id:int,username:str|None,first_name:str|None,defaults:UserSettings)->None:
        async with self._lock: await asyncio.to_thread(self._upsert_user,user_id,username,first_name,defaults)
    def _upsert_user(self,user_id:int,username:str|None,first_name:str|None,defaults:UserSettings)->None:
        now=time()
        with self._connect() as conn:
            conn.execute("INSERT INTO users VALUES(?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET username=excluded.username,first_name=excluded.first_name,last_seen=excluded.last_seen",(user_id,username,first_name,now,now))
            conn.execute("INSERT OR IGNORE INTO user_settings VALUES(?,?,?,?,?,?,?,?)",(user_id,defaults.profile,defaults.clip_count,defaults.clip_duration,defaults.vertical_mode,int(defaults.subtitles),int(defaults.music),now))
    async def get_settings(self,user_id:int,defaults:UserSettings)->UserSettings:
        return await asyncio.to_thread(self._get_settings,user_id,defaults)
    def _get_settings(self,user_id:int,defaults:UserSettings)->UserSettings:
        with self._connect() as conn: row=conn.execute("SELECT * FROM user_settings WHERE user_id=?",(user_id,)).fetchone()
        if not row: return defaults
        return UserSettings(row["profile"],row["clip_count"],row["clip_duration"],row["vertical_mode"],bool(row["subtitles"]),bool(row["music"]))
    async def update_settings(self,user_id:int,settings:UserSettings)->None:
        async with self._lock: await asyncio.to_thread(self._update_settings,user_id,settings)
    def _update_settings(self,user_id:int,s:UserSettings)->None:
        with self._connect() as conn: conn.execute("UPDATE user_settings SET profile=?,clip_count=?,clip_duration=?,vertical_mode=?,subtitles=?,music=?,updated_at=? WHERE user_id=?",(s.profile,s.clip_count,s.clip_duration,s.vertical_mode,int(s.subtitles),int(s.music),time(),user_id))
    async def create_job(self,job:Job)->None:
        async with self._lock: await asyncio.to_thread(self._create_job,job)
    def _create_job(self,job:Job)->None:
        with self._connect() as conn: conn.execute("INSERT INTO jobs(id,user_id,chat_id,source_kind,source_value,status,settings_json,created_at,updated_at,error) VALUES(?,?,?,?,?,?,?,?,?,?)",(job.id,job.user_id,job.chat_id,job.source_kind,job.source_value,job.status.value,json.dumps(job.settings.to_dict()),job.created_at,job.created_at,job.error))
    async def set_status(self,job_id:str,status:JobStatus,error:str|None=None,analysis_path:Path|None=None,manifest_path:Path|None=None,output_count:int|None=None)->None:
        async with self._lock: await asyncio.to_thread(self._set_status,job_id,status,error,analysis_path,manifest_path,output_count)
    def _set_status(self,job_id:str,status:JobStatus,error:str|None,analysis_path:Path|None,manifest_path:Path|None,output_count:int|None)->None:
        fields=["status=?","updated_at=?","error=?"]; values:[Any]=[status.value,time(),error]
        if analysis_path is not None: fields.append("analysis_path=?"); values.append(str(analysis_path))
        if manifest_path is not None: fields.append("manifest_path=?"); values.append(str(manifest_path))
        if output_count is not None: fields.append("output_count=?"); values.append(output_count)
        values.append(job_id)
        with self._connect() as conn: conn.execute(f"UPDATE jobs SET {','.join(fields)} WHERE id=?",values)
    async def recent_jobs(self,user_id:int,limit:int=10)->list[dict[str,Any]]: return await asyncio.to_thread(self._recent_jobs,user_id,limit)
    def _recent_jobs(self,user_id:int,limit:int)->list[dict[str,Any]]:
        with self._connect() as conn: rows=conn.execute("SELECT * FROM jobs WHERE user_id=? ORDER BY created_at DESC LIMIT ?",(user_id,limit)).fetchall()
        return [dict(r) for r in rows]
    async def active_count(self,user_id:int)->int: return await asyncio.to_thread(self._active_count,user_id)
    def _active_count(self,user_id:int)->int:
        with self._connect() as conn: return int(conn.execute("SELECT COUNT(*) FROM jobs WHERE user_id=? AND status IN ('queued','downloading','validating','analyzing','transcribing','rendering','sending')",(user_id,)).fetchone()[0])
    async def resolve_prefix(self,user_id:int,prefix:str)->str|None: return await asyncio.to_thread(self._resolve_prefix,user_id,prefix)
    def _resolve_prefix(self,user_id:int,prefix:str)->str|None:
        with self._connect() as conn: rows=conn.execute("SELECT id FROM jobs WHERE user_id=? AND id LIKE ? AND status='queued' LIMIT 2",(user_id,f"{prefix}%")).fetchall()
        return str(rows[0][0]) if len(rows)==1 else None
    async def statistics(self)->dict[str,int]: return await asyncio.to_thread(self._statistics)
    def _statistics(self)->dict[str,int]:
        with self._connect() as conn:
            return {"users":int(conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]),"jobs":int(conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]),"active":int(conn.execute("SELECT COUNT(*) FROM jobs WHERE status IN ('queued','downloading','validating','analyzing','transcribing','rendering','sending')").fetchone()[0]),"completed":int(conn.execute("SELECT COUNT(*) FROM jobs WHERE status='completed'").fetchone()[0]),"failed":int(conn.execute("SELECT COUNT(*) FROM jobs WHERE status='failed'").fetchone()[0])}
