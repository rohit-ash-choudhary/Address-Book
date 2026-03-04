from sqlalchemy.orm import Session
from . import models

def get_addresses(db):
    return db.query(models.Address).all()

def get_address(db, address_id):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def create_address(db, name, street, city, latitude, longitude):
    a = models.Address(name=name, street=street, city=city, latitude=latitude, longitude=longitude)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def update_address(db, address_id, name, street, city, latitude, longitude):
    a = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not a:
        return None
    a.name = name
    a.street = street
    a.city = city
    a.latitude = latitude
    a.longitude = longitude
    db.commit()
    db.refresh(a)
    return a

def delete_address(db, address_id):
    a = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not a:
        return False
    db.delete(a)
    db.commit()
    return True
