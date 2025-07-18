from sqlalchemy.orm import Session
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripResponse
from app.encryption import EncryptionService
from app.config import load_config
from fastapi import HTTPException

config = load_config()
enc_service = EncryptionService(config.ENCRYPTION_PASSWORD)

def to_response(db_trip: Trip) -> TripResponse:
    return TripResponse(
        id=db_trip.id,
        date=db_trip.date,
        gross_earnings=enc_service.decrypt_float64(db_trip.gross_earnings_encrypted),
        miles_driven=db_trip.miles_driven,
        hours_worked=db_trip.hours_worked,
        gas_cost=enc_service.decrypt_float64(db_trip.gas_cost_encrypted),
        tolls=enc_service.decrypt_float64(db_trip.tolls_encrypted),
        created_at=db_trip.created_at,
        updated_at=db_trip.updated_at
    )

def create_trip(db: Session, trip: TripCreate):
    db_trip = Trip(
        date=trip.date,
        gross_earnings_encrypted=enc_service.encrypt_float64(trip.gross_earnings),
        miles_driven=trip.miles_driven,
        hours_worked=trip.hours_worked,
        gas_cost_encrypted=enc_service.encrypt_float64(trip.gas_cost),
        tolls_encrypted=enc_service.encrypt_float64(trip.tolls)
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return to_response(db_trip)

def update_trip(db: Session, trip_id: int, trip: TripCreate):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(404, "Trip not found")
    db_trip.date = trip.date
    db_trip.gross_earnings_encrypted = enc_service.encrypt_float64(trip.gross_earnings)
    db_trip.miles_driven = trip.miles_driven
    db_trip.hours_worked = trip.hours_worked
    db_trip.gas_cost_encrypted = enc_service.encrypt_float64(trip.gas_cost)
    db_trip.tolls_encrypted = enc_service.encrypt_float64(trip.tolls)
    db.commit()
    db.refresh(db_trip)
    return to_response(db_trip)

def get_trips(db: Session, skip: int = 0, limit: int = 100):
    trips = db.query(Trip).offset(skip).limit(limit).all()
    return [TripResponse(
        id=t.id,
        date=t.date,
        gross_earnings=enc_service.decrypt_float64(t.gross_earnings_encrypted),
        miles_driven=t.miles_driven,
        hours_worked=t.hours_worked,
        gas_cost=enc_service.decrypt_float64(t.gas_cost_encrypted),
        tolls=enc_service.decrypt_float64(t.tolls_encrypted),
        created_at=t.created_at,
        updated_at=t.updated_at
    ) for t in trips]

def delete_trip(db: Session, trip_id: int):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(404, "Trip not found")
    db.delete(db_trip)
    db.commit()