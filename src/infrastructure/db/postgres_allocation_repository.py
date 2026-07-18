import uuid
from typing import Dict, List

from sqlalchemy import select, tuple_

from src.core.entities.allocation import Allocation
from src.core.entities.allocation_filter import AllocationFilter
from src.infrastructure.db.database import async_session
from src.infrastructure.db.models import AllocationModel, RecordModel


class PostgresAllocationRepository:
    async def get_allocation_by_id(self, id: str) -> Allocation | None:
        id = id.strip().lower()
        async with async_session() as session:
            result = await session.execute(
                select(AllocationModel).where(AllocationModel.id == uuid.UUID(id))
            )
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_entity(model)

    async def list_allocations(
        self, limit: int, cursor: str | None = None
    ) -> List[Allocation]:
        async with async_session() as session:
            stmt = (
                select(AllocationModel)
                .join(AllocationModel.record)
                .order_by(RecordModel.released_date, AllocationModel.id)
            )

            if cursor is not None:
                cursor = cursor.strip().lower()
                cursor_uuid = uuid.UUID(cursor)
                cursor_result = await session.execute(
                    select(RecordModel.released_date)
                    .where(AllocationModel.id == cursor_uuid)
                    .join(AllocationModel.record)
                )
                cursor_released_date = cursor_result.scalar_one_or_none()
                if cursor_released_date is not None:
                    stmt = stmt.where(
                        tuple_(RecordModel.released_date, AllocationModel.id)
                        > (cursor_released_date, cursor_uuid)
                    )
                else:
                    stmt = stmt.where(AllocationModel.id > cursor_uuid)

            stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    async def list_allocations_by_filter(
        self,
        limit: int,
        filter: Dict[AllocationFilter, str],
        cursor: str | None = None,
    ) -> List[Allocation]:
        key, value = list(filter.items())[0]

        async with async_session() as session:
            stmt = (
                select(AllocationModel)
                .join(AllocationModel.record)
                .where(getattr(AllocationModel, key.value) == value)
                .order_by(RecordModel.released_date, AllocationModel.id)
            )

            if cursor is not None:
                cursor = cursor.strip().lower()
                cursor_uuid = uuid.UUID(cursor)
                cursor_result = await session.execute(
                    select(RecordModel.released_date)
                    .where(AllocationModel.id == cursor_uuid)
                    .join(AllocationModel.record)
                )
                cursor_released_date = cursor_result.scalar_one_or_none()
                if cursor_released_date is not None:
                    stmt = stmt.where(
                        tuple_(RecordModel.released_date, AllocationModel.id)
                        > (cursor_released_date, cursor_uuid)
                    )
                else:
                    stmt = stmt.where(AllocationModel.id > cursor_uuid)

            stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    def _to_entity(self, model: AllocationModel) -> Allocation:
        return Allocation(
            id=str(model.id),
            nca_number=model.nca_number,
            agency=model.agency,
            operating_unit=model.operating_unit,
            amount=model.amount,
        )
