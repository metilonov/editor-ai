from __future__ import annotations

import asyncio
import time
from pathlib import Path


def _cleanup(root:Path,older_hours:int)->int:
    if not root.exists(): return 0
    cutoff=time.time()-older_hours*3600; removed=0
    for path in root.iterdir():
        try:
            if path.stat().st_mtime<cutoff:
                if path.is_dir():
                    import shutil; shutil.rmtree(path,ignore_errors=True)
                else: path.unlink(missing_ok=True)
                removed+=1
        except OSError: pass
    return removed


async def cleanup_old(root:Path,older_hours:int)->int: return await asyncio.to_thread(_cleanup,root,older_hours)
