from pydantic import BaseModel


class Allocation(BaseModel):
    id: str
    nca_number: str  # reference for record
    agency: str
    operating_unit: str
    amount: float
