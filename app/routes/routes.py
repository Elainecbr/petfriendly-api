from fastapi import APIRouter
from app.schemas.place_schema import PlaceSchema
from app.models.place import Place
from app.database.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

router = APIRouter()

@router.get("/places", response_model=list[PlaceSchema])
def get_places(db: Session = Depends(get_db)):
    places = db.query(Place).all()
    return places

@router.post("/places", response_model=PlaceSchema)
def create_place(place: PlaceSchema, db: Session = Depends(get_db)):
    new_place = Place(**place.dict())
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place

@router.put("/places/{place_id}", response_model=PlaceSchema)
def update_place(place_id: int, place: PlaceSchema, db: Session = Depends(get_db)):
    existing_place = db.query(Place).filter(Place.id == place_id).first()
    if not existing_place:
        raise HTTPException(status_code=404, detail="Place not found")
    for key, value in place.dict().items():
        setattr(existing_place, key, value)
    db.commit()
    return existing_place

@router.delete("/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    existing_place = db.query(Place).filter(Place.id == place_id).first()
    if not existing_place:
        raise HTTPException(status_code=404, detail="Place not found")
    db.delete(existing_place)
    db.commit()
    return {"detail": "Place deleted successfully"}