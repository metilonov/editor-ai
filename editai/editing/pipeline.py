from __future__ import annotations

from pathlib import Path

from editai.domain.models import Candidate,MediaInfo,SubtitleSegment,UserSettings
from editai.domain.profiles import get_profile
from editai.editing.manifest import write_manifest
from editai.editing.music import choose_music
from editai.editing.renderer import render_clip
from editai.editing.subtitles import write_clip_srt
from editai.media.ffmpeg import make_thumbnail


async def render_all(source:Path,info:MediaInfo,segments:list[Candidate],subtitles:list[SubtitleSegment],settings:UserSettings,output_dir:Path,work_dir:Path,music_dir:Path)->tuple[list[Path],Path,Path|None]:
    output_dir.mkdir(parents=True,exist_ok=True); profile=get_profile(settings.profile); outputs=[]; clip_pairs=[]
    music=choose_music(music_dir,source.name) if settings.music else None
    for i,segment in enumerate(segments,1):
        srt=write_clip_srt(subtitles,segment.start,segment.end,work_dir/f"clip_{i:02}.srt") if settings.subtitles else None
        target=output_dir/f"clip_{i:02}_{settings.profile}.mp4"
        await render_clip(source,segment,target,profile,settings.vertical_mode,srt,music,info.has_audio)
        outputs.append(target); clip_pairs.append((segment,target))
    manifest=write_manifest(output_dir/"manifest.json",info,settings,clip_pairs)
    thumb=None
    if segments:
        try: thumb=await make_thumbnail(source,(segments[0].start+segments[0].end)/2,output_dir/"cover.jpg")
        except Exception: thumb=None
    return outputs,manifest,thumb
