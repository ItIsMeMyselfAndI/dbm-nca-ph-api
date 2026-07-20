from fastapi import APIRouter, Depends, HTTPException, status

from src.core.entities.release import Release
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.interfaces.async_record_repository import AsyncRecordRepository
from src.core.interfaces.async_release_repository import AsyncReleaseRepository
from src.core.use_cases.v2.pipeline.delete_release import DeleteRelease
from src.core.use_cases.v2.pipeline.upsert_release import UpsertRelease
from src.presentation.api.dependencies_v2 import (
    get_allocation_repository,
    get_record_repository,
    get_release_repository,
)
from src.presentation.api.schemas import ReleaseCreate

router = APIRouter(prefix="/releases")


@router.post("", status_code=status.HTTP_201_CREATED)
async def upsert_release(
    data: ReleaseCreate,
    release_repo: AsyncReleaseRepository = Depends(get_release_repository),
):
    try:
        use_case = UpsertRelease(release_repo)
        release = await use_case.execute(Release(**data.model_dump()))
        return release
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_release(
    id: str,
    release_repo: AsyncReleaseRepository = Depends(get_release_repository),
    record_repo: AsyncRecordRepository = Depends(get_record_repository),
    allocation_repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = DeleteRelease(release_repo, record_repo, allocation_repo)
        await use_case.execute(id)
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
