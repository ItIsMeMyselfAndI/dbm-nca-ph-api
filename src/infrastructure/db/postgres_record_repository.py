import uuid
from typing import Dict, List

from sqlalchemy import select, tuple_

from src.core.entities.record import Record
from src.core.entities.record_filter import RecordFilter
from src.infrastructure.db.database import async_session
from src.infrastructure.db.models import RecordModel


class PostgresRecordRepository:
    async def get_record_by_id(self, id: str) -> Record | None:
        id = id.strip().lower()
        async with async_session() as session:
            result = await session.execute(
                select(RecordModel).where(RecordModel.id == uuid.UUID(id))
            )
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_entity(model)

    async def list_records(
        self, limit: int, cursor: str | None = None
    ) -> List[Record]:
        async with async_session() as session:
            stmt = select(RecordModel).order_by(RecordModel.released_date, RecordModel.id)

            if cursor is not None:
                cursor = cursor.strip().lower()
                cursor_uuid = uuid.UUID(cursor)
                cursor_result = await session.execute(
                    select(RecordModel.released_date).where(RecordModel.id == cursor_uuid)
                )
                cursor_released_date = cursor_result.scalar_one_or_none()
                if cursor_released_date is not None:
                    stmt = stmt.where(
                        tuple_(RecordModel.released_date, RecordModel.id)
                        > (cursor_released_date, cursor_uuid)
                    )
                else:
                    stmt = stmt.where(RecordModel.id > cursor_uuid)

            stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    async def list_records_by_filter(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> List[Record]:
        key, value = list(filter.items())[0]

        async with async_session() as session:
            stmt = (
                select(RecordModel)
                .where(getattr(RecordModel, key.value) == value)
                .order_by(RecordModel.released_date, RecordModel.id)
            )

            if cursor is not None:
                cursor = cursor.strip().lower()
                cursor_uuid = uuid.UUID(cursor)
                cursor_result = await session.execute(
                    select(RecordModel.released_date).where(RecordModel.id == cursor_uuid)
                )
                cursor_released_date = cursor_result.scalar_one_or_none()
                if cursor_released_date is not None:
                    stmt = stmt.where(
                        tuple_(RecordModel.released_date, RecordModel.id)
                        > (cursor_released_date, cursor_uuid)
                    )
                else:
                    stmt = stmt.where(RecordModel.id > cursor_uuid)

            stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    def _to_entity(self, model: RecordModel) -> Record:
        return Record(
            id=str(model.id),
            nca_number=model.nca_number,
            nca_type=model.nca_type,
            released_date=model.released_date,
            department=model.department,
            purpose=model.purpose,
            release_id=model.release_id,
        )
