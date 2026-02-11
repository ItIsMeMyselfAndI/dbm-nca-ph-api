from pydantic import BaseModel


class Record(BaseModel):
    id: str
    nca_number: str
    nca_type: str
    released_date: str
    department: str
    purpose: str
    release_id: str
