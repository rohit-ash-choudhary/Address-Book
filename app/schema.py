from typing import Optional
from pydantic import BaseModel, field_validator

def check_lat(v):
    if v is None:
        return v
    if not -90 <= v <= 90:
        raise ValueError("latitude -90 to 90")
    return v

def check_lon(v):
    if v is None:
        return v
    if not -180 <= v <= 180:
        raise ValueError("longitude -180 to 180")
    return v

def check_str(v):
    s = (v or "").strip()
    if not s:
        raise ValueError("required")
    return s

class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("name", "street", "city")
    @classmethod
    def v_str(cls, v):
        return check_str(v)

    @field_validator("latitude")
    @classmethod
    def v_lat(cls, v):
        return check_lat(v)

    @field_validator("longitude")
    @classmethod
    def v_lon(cls, v):
        return check_lon(v)

class AddressResponse(BaseModel):
    id: int
    name: str
    street: str
    city: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True
