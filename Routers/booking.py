from .. import models, schemas
from .. import crud
from ..get_db import get_db
from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter()

@router.post('/bookings/{guest_id}/')
async def create_booking(booking: schemas.BookingCreate,guest_id: int, db: Session = Depends(get_db)):
    if not crud.get_guest(db=db, guest_id=guest_id):
        raise HTTPException(status_code=404, detail='This email is not registered.')
    if not crud.get_room(db=db, room_id=booking.room_id):
        raise HTTPException(status_code=404, detail='This room ID is not registered.')
    if crud.is_room_reserved(db=db, room_id=booking.room_id, check_in_date=booking.check_in_date, check_out_date=booking.check_out_date):
        raise HTTPException(status_code=400, detail='This room is reserved for this period.')
    
    db_price_per_night = crud.get_price_per_night(room_id=booking.room_id, db=db)
    if not db_price_per_night:
        raise HTTPException(status_code=404, detail='This room ID does not exist.')
    return crud.create_booking(db=db, booking=booking, price_per_night=db_price_per_night, guest_id=guest_id)

@router.get('/bookings/{booking_id}/', response_model=schemas.Booking)
async def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db=db, booking_id=booking_id)
    
    if not db_booking:
        raise HTTPException(status_code=404, detail='This booking is not registered.')
    
    return db_booking

@router.delete('/bookings/{booking_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    
    db_booking = crud.delete_booking(db=db, booking_id=booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail='This booking ID does not exist.')
    return

@router.patch('/bookings/{booking_id}/', response_model=schemas.Booking)
async def patch_booking(booking_id: int, booking_update: schemas.BookingUpdate, db: Session = Depends(get_db)):
    db_booking = crud.patch_booking(db=db, booking_id=booking_id, booking_update=booking_update)
    if not db_booking:
        raise HTTPException(status_code=404, detail="This booking ID does not exist.")
    return db_booking