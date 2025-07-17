from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trip import TripCreate, TripResponse
from app.crud.trip import create_trip, get_trips, update_trip, delete_trip
from app.auth.middleware import get_current_user

router = APIRouter()

@router.post("/", response_model=TripResponse)
def create(trip: TripCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_trip(db, trip)

@router.get("/", response_model=list[TripResponse])
def read(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_trips(db, skip, limit)

@router.put("/{trip_id}", response_model=TripResponse)
def update(trip_id: int, trip: TripCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return update_trip(db, trip_id, trip)

@router.delete("/{trip_id}", response_model=dict)
def delete(trip_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    delete_trip(db, trip_id)
    return {"detail": "Trip deleted"}