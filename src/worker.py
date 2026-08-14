import asyncio
import time
from .outbox import process_outbox_batch
from .config import settings

async def worker_loop():
    while True:
        try:
            processed = await process_outbox_batch(settings.OUTBOX_BATCH_SIZE)
            if processed == 0:
                await asyncio.sleep(settings.OUTBOX_POLL_INTERVAL)
            # else continue immediately to process more
        except Exception as e:
            print(f"Worker error: {e}")
            await asyncio.sleep(settings.OUTBOX_POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(worker_loop())
