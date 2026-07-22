from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from typing import TypeVar

T = TypeVar("T")


async def gather_limited(limit: int, *aws: Awaitable[T]) -> list[T]:
    semaphore = asyncio.Semaphore(max(1, limit))
    async def run(aw: Awaitable[T]) -> T:
        async with semaphore: return await aw
    return list(await asyncio.gather(*(run(aw) for aw in aws)))
