from typing import List

from sqlalchemy import select

from src.core.entities.release import Release
from src.infrastructure.db.database import async_session
from src.infrastructure.db.models import ReleaseModel


class PostgresReleaseRepository:
    async def get_release_by_id(self, id: str) -> Release | None:
        id = id.strip().lower()
        async with async_session() as session:
            result = await session.execute(select(ReleaseModel).where(ReleaseModel.id == id))
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._to_entity(model)

    async def list_releases(
        self, limit: int, cursor: str | None = None
    ) -> List[Release]:
        async with async_session() as session:
            stmt = select(ReleaseModel).order_by(ReleaseModel.id)

            if cursor is not None:
                cursor = cursor.strip().lower()
                stmt = stmt.where(ReleaseModel.id > cursor)

            stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    async def create_release(self, release: Release) -> Release:
        async with async_session() as session:
            model = ReleaseModel(
                id=release.id,
                title=release.title,
                url=release.url,
                filename=release.filename,
                year=release.year,
                page_count=release.page_count,
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def update_release(self, id: str, release: Release) -> Release | None:
        async with async_session() as session:
            model = await session.get(ReleaseModel, id)
            if model is None:
                return None
            model.title = release.title
            model.url = release.url
            model.filename = release.filename
            model.year = release.year
            model.page_count = release.page_count
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def delete_release(self, id: str) -> bool:
        async with async_session() as session:
            model = await session.get(ReleaseModel, id)
            if model is None:
                return False
            await session.delete(model)
            await session.commit()
            return True

    def _to_entity(self, model: ReleaseModel) -> Release:
        return Release(
            id=model.id,
            title=model.title,
            url=model.url,
            filename=model.filename,
            year=model.year,
            page_count=model.page_count,
            file_meta_created_at=str(model.file_meta_created_at) if model.file_meta_created_at else None,
            file_meta_modified_at=str(model.file_meta_modified_at) if model.file_meta_modified_at else None,
        )
