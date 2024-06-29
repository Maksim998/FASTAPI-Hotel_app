from .. import models, schemas
from .. import crud
from ..get_db import get_db
from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter()

@router.post('/payments/{booking_id}/', response_model=schemas.Payment)
async def create_payment(payment: schemas.PaymentCreate, booking_id: int, db: Session = Depends(get_db)):
    if not crud.get_booking(db=db, booking_id=booking_id):
        raise HTTPException(status_code=404, detail='This booking is not registered.')
    
    if crud.get_payment_by_booking_id(db=db, booking_id=booking_id):
        raise HTTPException(status_code=400, detail=f'Payment for booking ID: {booking_id} already created.')

    return crud.create_payment(db=db, payment=payment, booking_id=booking_id)

@router.get('/payments/{payment_id}/', response_model= schemas.Payment)
async def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db=db, payment_id=payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail='Payment is not registered.')
    
    return db_payment

@router.delete('/payments/{payment_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = crud.delete_payment(db=db, payment_id=payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail='This payment ID does not exist.')
    return

@router.patch('/payments/{payment_id}/', response_model=schemas.Payment)
async def payment_patch(payment_id: int, payment_update: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = crud.patch_payment(db=db, payment_id=payment_id, payment_update=payment_update)
    if not db_payment:
        raise HTTPException(status_code=400, detail='This paymet ID does not exist.')
    return db_payment