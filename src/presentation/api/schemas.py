from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class CursorPageResponse(BaseModel, Generic[T]):
    items: List[T]
    count: int
    cursor: Optional[str]
    next_cursor: Optional[str]


class ReleaseResponse(BaseModel):
    id: str
    year: int
    url: str
    filename: str


class ReleaseCreate(BaseModel):
    id: str
    title: str
    url: str
    filename: str
    year: int
    page_count: int = 0


class RecordResponse(BaseModel):
    id: str
    nca_number: str
    nca_type: str
    released_date: Optional[str]
    department: Optional[str]
    purpose: Optional[str]
    release_id: str


class RecordCreate(BaseModel):
    nca_number: str
    nca_type: str
    released_date: str
    department: str
    purpose: str
    release_id: str


class AllocationResponse(BaseModel):
    id: str
    nca_number: str  # reference for record
    agency: Optional[str]
    operating_unit: Optional[str]
    amount: float


class AllocationCreate(BaseModel):
    nca_number: str
    agency: str
    operating_unit: str
    amount: float


class EndpointInfo(BaseModel):
    method: str
    path: str
    description: str


class IndexResponse(BaseModel):
    title: str
    version: str
    description: str
    endpoints: list[EndpointInfo]
    docs_url: str
