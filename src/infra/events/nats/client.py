from contextlib import asynccontextmanager

import nats

from src.config.envirenment import get_settings

_S = get_settings()


@asynccontextmanager
async def nats_connection():
    nc = None
    try:
        nc = await nats.connect(_S.NATS_URL)
        yield nc
    finally:
        await nc.close()
