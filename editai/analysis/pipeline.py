from __future__ import annotations

import asyncio
from pathlib import Path

from editai.analysis.audio import analyze_audio
from editai.analysis.candidates import generate_candidates
from editai.analysis.diversity import select_diverse
from editai.analysis.report import write_report
from editai.analysis.sampling import normalize_series
from editai.analysis.scenes import detect_scenes
from editai.analysis.scoring import score_all
from editai.analysis.visual import analyze_visual
from editai.domain.models import Candidate,FeatureBundle,MediaInfo
from editai.domain.profiles import get_profile


async def analyze(source:Path,info:MediaInfo,work_dir:Path,profile_key:str,clip_duration:int,clip_count:int)->tuple[list[Candidate],FeatureBundle,Path|None,Path]:
    work_dir.mkdir(parents=True,exist_ok=True)
    scenes_task=asyncio.create_task(detect_scenes(source)); visual_task=asyncio.create_task(analyze_visual(source)); audio_task=asyncio.create_task(analyze_audio(source,work_dir,info.has_audio))
    scenes,visual,(rms,peaks,wav)=await asyncio.gather(scenes_task,visual_task,audio_task)
    bundle=FeatureBundle(scenes=scenes,motion=normalize_series(visual.motion),audio_rms=normalize_series(rms),audio_peaks=normalize_series(peaks),faces=normalize_series(visual.faces),sharpness=visual.sharpness,brightness=visual.brightness,saturation=visual.saturation,entropy=visual.entropy)
    candidates=generate_candidates(info.duration,bundle,clip_duration,min(10,clip_duration))
    scored=score_all(candidates,bundle,get_profile(profile_key)); selected=select_diverse(scored,clip_count)
    report=write_report(work_dir/"analysis.json",info,bundle,scored,selected,profile_key)
    return selected,bundle,wav,report
