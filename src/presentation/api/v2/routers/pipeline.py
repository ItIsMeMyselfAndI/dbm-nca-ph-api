import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.core.entities.allocation import Allocation
from src.core.entities.record import Record
from src.core.entities.release import Release
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.interfaces.async_record_repository import AsyncRecordRepository
from src.core.interfaces.async_release_repository import AsyncReleaseRepository
from src.core.use_cases.v2.pipeline.delete_allocation import DeleteAllocation
from src.core.use_cases.v2.pipeline.delete_record import DeleteRecord
from src.core.use_cases.v2.pipeline.delete_release import DeleteRelease
from src.core.use_cases.v2.pipeline.upsert_allocation import UpsertAllocation
from src.core.use_cases.v2.pipeline.upsert_record import UpsertRecord
from src.core.use_cases.v2.pipeline.upsert_release import UpsertRelease
from src.presentation.api.auth import require_pipeline_key
from src.presentation.api.dependencies_v2 import (
    get_allocation_repository,
    get_record_repository,
    get_release_repository,
)
from src.presentation.api.schemas import AllocationCreate, RecordCreate, ReleaseCreate

router = APIRouter(
    prefix="/pipeline",
    dependencies=[Depends(require_pipeline_key)],
)


@router.post("/releases")
async def upsert_release(
    data: ReleaseCreate,
    response: Response,
    release_repo: AsyncReleaseRepository = Depends(get_release_repository),
):
    try:
        use_case = UpsertRelease(release_repo)
        release, was_created = await use_case.execute(Release(**data.model_dump()))
        if was_created:
            response.status_code = status.HTTP_201_CREATED
        return release
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/releases/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.post("/records")
async def upsert_record(
    data: RecordCreate,
    response: Response,
    record_repo: AsyncRecordRepository = Depends(get_record_repository),
):
    try:
        use_case = UpsertRecord(record_repo)
        record, was_created = await use_case.execute(
            Record(id=str(uuid.uuid4()), **data.model_dump())
        )
        if was_created:
            response.status_code = status.HTTP_201_CREATED
        return record
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/records/{nca_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    nca_number: str,
    record_repo: AsyncRecordRepository = Depends(get_record_repository),
    allocation_repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = DeleteRecord(record_repo, allocation_repo)
        await use_case.execute(nca_number)
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/allocations")
async def upsert_allocation(
    data: AllocationCreate,
    response: Response,
    allocation_repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = UpsertAllocation(allocation_repo)
        allocation, was_created = await use_case.execute(
            Allocation(id=str(uuid.uuid4()), **data.model_dump())
        )
        if was_created:
            response.status_code = status.HTTP_201_CREATED
        return allocation
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/allocations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_allocation(
    id: str,
    allocation_repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = DeleteAllocation(allocation_repo)
        await use_case.execute(id)
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
