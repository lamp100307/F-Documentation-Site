import asyncio

from bin.bot import run_bot
from bin.backend import run_backend

async def main():
    await asyncio.gather(run_bot(), run_backend())

if __name__ == "__main__":
    asyncio.run(main())
