import asyncio
import logging


logger = logging.getLogger(__name__)


async def dummy_job():
    while True:
        logger.debug("im dummy job")
        await asyncio.sleep(2)
