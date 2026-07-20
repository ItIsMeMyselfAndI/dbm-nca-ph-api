from fastapi import APIRouter, Depends, HTTPException

from src.core.entities.record_filter import RecordFilter

from src.core.interfaces.record_repository import RecordRepository

from src.core.use_cases.v1.record.get_record_by_id import GetRecordByID
from src.core.use_cases.v1.record.list_records import ListRecords
from src.core.use_cases.v1.record.list_records_by_filter import ListRecordsByFilter

from src.presentation.api.schemas import CursorPageResponse, RecordResponse
from src.presentation.api.dependencies import get_record_repository

router = APIRouter(prefix="/records")


@router.get("", response_model=CursorPageResponse[RecordResponse])
def list_records(
    cursor: str | None = None,
    limit: int = 20,
    repo: RecordRepository = Depends(get_record_repository),
):
    try:
        use_case = ListRecords(repo)
        records, next_cursor = use_case.execute(cursor=cursor, limit=limit)

        response = CursorPageResponse(
            items=records,
            count=len(records),
            cursor=cursor,
            next_cursor=next_cursor,
        )
        return response

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=RecordResponse)
def get_record_by_id(
    id: str,
    repo: RecordRepository = Depends(get_record_repository),
):
    try:
        use_case = GetRecordByID(repo)
        record = use_case.execute(id)
        return record

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{filter_key}/{filter_value}", response_model=CursorPageResponse[RecordResponse]
)
def list_records_by_filter(
    filter_key: RecordFilter,
    filter_value: str,
    cursor: str | None = None,
    limit: int = 20,
    repo: RecordRepository = Depends(get_record_repository),
):
    try:
        use_case = ListRecordsByFilter(repo)

        filter = {filter_key: filter_value}
        records, next_cursor = use_case.execute(
            cursor=cursor, filter=filter, limit=limit
        )

        response = CursorPageResponse(
            items=records,
            count=len(records),
            cursor=cursor,
            next_cursor=next_cursor,
        )
        return response

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
