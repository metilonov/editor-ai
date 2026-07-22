from __future__ import annotations

import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


async def run_process(*args: str, timeout: float | None = None) -> tuple[str, str]:
    logger.debug("exec: %s", " ".join(args))
    proc = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except TimeoutError:
        proc.kill(); await proc.wait(); raise RuntimeError(f"Команда превысила timeout: {args[0]}")
    out, err = stdout.decode(errors="replace"), stderr.decode(errors="replace")
    if proc.returncode:
        raise RuntimeError(f"{args[0]} завершился с кодом {proc.returncode}: {err[-1500:]}")
    return out, err
