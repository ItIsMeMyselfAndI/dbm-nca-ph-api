import asyncio

from src.infrastructure.db.database import engine
from src.infrastructure.db.models import Base


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")


asyncio.run(main())
