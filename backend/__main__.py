import asyncio

from backend.bin.bot import run_bot
from backend.bin.backend import run_backend

async def main():
    await asyncio.gather(run_bot(), run_backend())

if __name__ == "__main__":
    asyncio.run(main())
