from src.infrastructure.db.database import async_session
from src.infrastructure.db.postgres_allocation_repository import (
    PostgresAllocationRepository,
)
from src.infrastructure.db.postgres_record_repository import PostgresRecordRepository
from src.infrastructure.db.postgres_release_repository import (
    PostgresReleaseRepository,
)


async def get_db_session():
    async with async_session() as session:
        yield session


def get_release_repository() -> PostgresReleaseRepository:
    return PostgresReleaseRepository()


def get_record_repository() -> PostgresRecordRepository:
    return PostgresRecordRepository()


def get_allocation_repository() -> PostgresAllocationRepository:
    return PostgresAllocationRepository()
