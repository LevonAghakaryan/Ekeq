from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    customer_name: str
    phone_number: str
    preferred_contact: str
    template_id: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True