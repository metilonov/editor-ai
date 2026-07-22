from __future__ import annotations

from pathlib import Path

from editai.domain.models import Candidate,MediaInfo,UserSettings
from editai.utils.jsonio import dump_json


def write_manifest(path:Path,info:MediaInfo,settings:UserSettings,clips:list[tuple[Candidate,Path]])->Path:
    return dump_json(path,{"source":str(info.path),"duration":info.duration,"settings":settings,"clips":[{"segment":c,"file":str(p)} for c,p in clips]})
