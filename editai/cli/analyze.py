from __future__ import annotations

import asyncio
from pathlib import Path

from editai.analysis.pipeline import analyze
from editai.core.config import load_settings
from editai.media.validation import validate_media


async def analyze_file(path:Path,profile:str="dynamic",clips:int=3,duration:int=30)->int:
    settings=load_settings(require_token=False);info=await validate_media(path,settings);selected,_,_,report=await analyze(path,info,settings.temp_dir/"cli_analysis",profile,duration,clips)
    print("Report:",report)
    for i,c in enumerate(selected,1):print(i,round(c.start,2),round(c.end,2),round(c.score,3),c.reasons)
    return 0
