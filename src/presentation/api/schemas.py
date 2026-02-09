from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class CursorPageResponse(BaseModel, Generic[T]):
    items: List[T]
    cusor: int
    next_cursor: Optional[int]
    has_more: bool


class ReleaseResponse(BaseModel):
    id: str
    year: int
    url: str
    filename: str


class RecordResponse(BaseModel):
    id: str
    nca_number: str
    nca_type: str
    released_date: Optional[str]
    department: Optional[str]
    purpose: Optional[str]
    release_id: str


class AllocationResponse(BaseModel):
    id: str
    nca_number: str  # reference for record
    agency: Optional[str]
    operating_unit: Optional[str]
    amount: float
