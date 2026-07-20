from os import environ

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.config import settings

_pool_kwargs = {}
if environ.get("ASYNC_POOL_DISABLED"):
    from sqlalchemy.pool import NullPool
    _pool_kwargs["poolclass"] = NullPool
else:
    _pool_kwargs["pool_pre_ping"] = True

engine = create_async_engine(settings.DATABASE_URL, **_pool_kwargs)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
