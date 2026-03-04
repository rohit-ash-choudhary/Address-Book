from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import crud, schema, geocode

router = APIRouter(prefix="/addresses", tags=["addresses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_lat_lon(addr: schema.AddressCreate):
    if addr.latitude is not None and addr.longitude is not None:
        return addr.latitude, addr.longitude
    try:
        return geocode.geocode_address(addr.street, addr.city)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/", response_model=List[schema.AddressResponse])
def list_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db)

@router.post("/", response_model=schema.AddressResponse)
def create_address(addr: schema.AddressCreate, db: Session = Depends(get_db)):
    lat, lon = get_lat_lon(addr)
    return crud.create_address(db, addr.name, addr.street, addr.city, lat, lon)

# before {address_id} so "distance" is not taken as id
@router.get("/distance")
def distance(
    from_id: int = Query(..., alias="from_id"),
    to_id: Optional[int] = Query(None, alias="to_id"),
    to_lat: Optional[float] = Query(None),
    to_lon: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    from geopy.distance import geodesic

    if to_id:
        a1 = crud.get_address(db, from_id)
        a2 = crud.get_address(db, to_id)
        if not a1:
            raise HTTPException(404, "Source not found")
        if not a2:
            raise HTTPException(404, "Target not found")
        p1 = (a1.latitude, a1.longitude)
        p2 = (a2.latitude, a2.longitude)
    else:
        if to_lat is None or to_lon is None:
            raise HTTPException(400, "Need to_id or to_lat and to_lon")
        a1 = crud.get_address(db, from_id)
        if not a1:
            raise HTTPException(404, "Source not found")
        p1 = (a1.latitude, a1.longitude)
        p2 = (to_lat, to_lon)

    km = geodesic(p1, p2).kilometers
    return {"distance_km": round(km, 2), "from_address_id": from_id}

@router.get("/{address_id}", response_model=schema.AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    a = crud.get_address(db, address_id)
    if not a:
        raise HTTPException(404, "Address not found")
    return a

@router.put("/{address_id}", response_model=schema.AddressResponse)
def update_address(address_id: int, addr: schema.AddressCreate, db: Session = Depends(get_db)):
    lat, lon = get_lat_lon(addr)
    a = crud.update_address(db, address_id, addr.name, addr.street, addr.city, lat, lon)
    if not a:
        raise HTTPException(404, "Address not found")
    return a

@router.delete("/{address_id}", status_code=204)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_address(db, address_id)
    if not ok:
        raise HTTPException(404, "Address not found")
