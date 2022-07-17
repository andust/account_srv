from contextlib import asynccontextmanager

import nats

from src.config.envirenment import get_settings

_S = get_settings()


async def error_cb(err):
    print("error_cb", err)


@asynccontextmanager
async def nats_connection():
    nc = None
    try:
        nc = await nats.connect(_S.NATS_URL, name="acccount_connect", error_cb=error_cb)
        yield nc
    finally:
        if nc:
            await nc.close()
