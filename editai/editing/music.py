from __future__ import annotations

import hashlib
from pathlib import Path

from editai.utils.files import list_music


def choose_music(library:Path,seed:str)->Path|None:
    tracks=list_music(library)
    if not tracks: return None
    index=int(hashlib.sha256(seed.encode()).hexdigest()[:8],16)%len(tracks)
    return tracks[index]
