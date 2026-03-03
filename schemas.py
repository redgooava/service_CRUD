"""
Схемы для валицации на Pydantic
"""

from typing import List

from pydantic import BaseModel


class Datatables(BaseModel):
    db_id: int
    rate_id: int
    rate_name: str
    service_id: int
    service_name: str
    price: int

    class Config:
        from_attributes = True


class DataGetResponse(BaseModel):
    data: List[Datatables]


class DataPostRequest(BaseModel):
    db_id: int
    rate_id: int
    rate_name: str
    service_id: int
    service_name: str
    price: int


class DataPostResponse(BaseModel):
    message: str
