import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.entities.record import Record
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.interfaces.async_record_repository import AsyncRecordRepository
from src.core.use_cases.v2.pipeline.delete_record import DeleteRecord
from src.core.use_cases.v2.pipeline.upsert_record import UpsertRecord
from src.presentation.api.dependencies_v2 import (
    get_allocation_repository,
    get_record_repository,
)
from src.presentation.api.schemas import RecordCreate

router = APIRouter(prefix="/records")


@router.post("", status_code=status.HTTP_201_CREATED)
async def upsert_record(
    data: RecordCreate,
    record_repo: AsyncRecordRepository = Depends(get_record_repository),
):
    try:
        use_case = UpsertRecord(record_repo)
        record = await use_case.execute(
            Record(id=str(uuid.uuid4()), **data.model_dump())
        )
        return record
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{nca_number}", status_code=status.HTTP_204_NO_CONTENT)
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
