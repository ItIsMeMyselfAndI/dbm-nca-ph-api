import asyncio
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.allocation import Allocation
from src.core.entities.record import Record
from src.core.entities.release import Release
from src.infrastructure.db.database import async_session
from src.infrastructure.db.models import AllocationModel, RecordModel, ReleaseModel
from src.infrastructure.db.supabase_allocation_repository import (
    SupabaseAllocationRepository,
)
from src.infrastructure.db.supabase_record_repository import SupabaseRecordRepository
from src.infrastructure.db.supabase_release_repository import SupabaseReleaseRepository

BATCH_SIZE = 1000


def _fetch_all_releases() -> List[Release]:
    repo = SupabaseReleaseRepository()
    items: List[Release] = []
    cursor: str | None = None
    while True:
        batch = repo.list_releases(limit=BATCH_SIZE, cursor=cursor)
        if not batch:
            break
        items.extend(batch)
        cursor = batch[-1].id
        print(f"  Fetched {len(items)} releases...")
    return items


def _fetch_all_records() -> List[Record]:
    repo = SupabaseRecordRepository()
    items: List[Record] = []
    cursor: str | None = None
    while True:
        batch = repo.list_records(limit=BATCH_SIZE, cursor=cursor)
        if not batch:
            break
        items.extend(batch)
        cursor = batch[-1].id
        print(f"  Fetched {len(items)} records...")
    return items


def _fetch_all_allocations() -> List[Allocation]:
    repo = SupabaseAllocationRepository()
    items: List[Allocation] = []
    cursor: str | None = None
    while True:
        batch = repo.list_allocations(limit=BATCH_SIZE, cursor=cursor)
        if not batch:
            break
        items.extend(batch)
        cursor = batch[-1].id
        print(f"  Fetched {len(items)} allocations...")
    return items


async def _clear_tables(session: AsyncSession):
    await session.execute(delete(AllocationModel))
    await session.execute(delete(RecordModel))
    await session.execute(delete(ReleaseModel))
    await session.commit()


async def _insert_releases(session: AsyncSession, releases: List[Release]):
    for i, r in enumerate(releases):
        session.add(
            ReleaseModel(
                id=r.id,
                title=r.title,
                url=r.url,
                filename=r.filename,
                year=r.year,
                page_count=r.page_count,
                file_meta_created_at=r.file_meta_created_at,
                file_meta_modified_at=r.file_meta_modified_at,
            )
        )
        if (i + 1) % 500 == 0:
            await session.flush()
    await session.commit()
    print(f"  Inserted {len(releases)} releases.")


async def _insert_records(session: AsyncSession, records: List[Record]):
    for i, r in enumerate(records):
        session.add(
            RecordModel(
                id=r.id,
                nca_number=r.nca_number,
                nca_type=r.nca_type,
                department=r.department,
                released_date=r.released_date,
                purpose=r.purpose,
                release_id=r.release_id,
            )
        )
        if (i + 1) % 500 == 0:
            await session.flush()
    await session.commit()
    print(f"  Inserted {len(records)} records.")


async def _insert_allocations(session: AsyncSession, allocations: List[Allocation]):
    for i, a in enumerate(allocations):
        session.add(
            AllocationModel(
                id=a.id,
                nca_number=a.nca_number,
                agency=a.agency,
                operating_unit=a.operating_unit,
                amount=a.amount,
            )
        )
        if (i + 1) % 500 == 0:
            await session.flush()
    await session.commit()
    print(f"  Inserted {len(allocations)} allocations.")


async def main():
    print("Fetching data from Supabase (v1)...")
    releases = await asyncio.to_thread(_fetch_all_releases)
    records = await asyncio.to_thread(_fetch_all_records)
    allocations = await asyncio.to_thread(_fetch_all_allocations)
    print(f"Fetched: {len(releases)} releases, {len(records)} records, {len(allocations)} allocations")

    print("Writing to local Postgres (v2)...")
    async with async_session() as session:
        await _clear_tables(session)
        await _insert_releases(session, releases)
        await _insert_records(session, records)
        await _insert_allocations(session, allocations)

    print("Seed complete.")


asyncio.run(main())
