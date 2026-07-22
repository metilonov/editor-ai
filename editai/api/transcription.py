from __future__ import annotations

import json
from pathlib import Path

import aiohttp

from editai.domain.models import SubtitleSegment


class TranscriptionClient:
    def __init__(self,url:str|None,key:str|None,model:str,language:str)->None:
        self.url=url; self.key=key; self.model=model; self.language=language

    @property
    def enabled(self)->bool: return bool(self.url and self.key)

    async def transcribe(self,audio:Path)->list[SubtitleSegment]:
        if not self.enabled: return []
        form=aiohttp.FormData(); form.add_field("model",self.model); form.add_field("language",self.language); form.add_field("response_format","verbose_json")
        headers={"Authorization":f"Bearer {self.key}"}
        with audio.open("rb") as f:
            form.add_field("file",f,filename=audio.name,content_type="audio/wav")
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1800)) as session:
                async with session.post(self.url,headers=headers,data=form) as response:
                    text=await response.text()
                    if response.status>=400: raise RuntimeError(f"STT API {response.status}: {text[:400]}")
        payload=json.loads(text); result=[]
        for item in payload.get("segments") or []:
            text=str(item.get("text") or "").strip()
            if text: result.append(SubtitleSegment(float(item.get("start") or 0),float(item.get("end") or 0),text))
        return result
