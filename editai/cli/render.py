from __future__ import annotations

from pathlib import Path

from editai.analysis.pipeline import analyze
from editai.core.config import load_settings
from editai.domain.models import UserSettings
from editai.editing.pipeline import render_all
from editai.media.validation import validate_media


async def render_file(path:Path,profile:str="dynamic",clips:int=3,duration:int=30,vertical:str="blur")->int:
    settings=load_settings(require_token=False);info=await validate_media(path,settings);work=settings.temp_dir/"cli_render";selected,_,_,_=await analyze(path,info,work,profile,duration,clips)
    outputs,manifest,_=await render_all(path,info,selected,[],UserSettings(profile,clips,duration,vertical,False,False),settings.output_dir/"cli",work,Path("assets/music").resolve())
    print("Outputs:");[print(x) for x in outputs];print("Manifest:",manifest);return 0
