from .. import models, schemas
from .. import crud
from ..get_db import get_db
from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter()

@router.post('/guests/', response_model= schemas.Guest)
async def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    
    if crud.get_guest_by_email(db=db, guest_email=guest.email):
        raise HTTPException(status_code=400, detail='Email already registered.')
    
    return crud.create_guest(db = db, guest=guest)

@router.get('/guests/', response_model = list[schemas.Guest])
async def read_all_guests(db: Session = Depends(get_db)):
    return crud.get_all_guests(db)

@router.get('/guests/id/{guest_id}/', response_model=schemas.Guest)
async def read_guest_by_id(guest_id: int, db: Session = Depends(get_db)):
    db_guest = crud.get_guest(guest_id=guest_id, db=db)
    if db_guest is None:
        raise HTTPException(status_code=404, detail='This guest ID does not exist.')
    return db_guest

@router.get('/guests/email/{guest_email}/', response_model=schemas.Guest)
async def read_guest_by_email(guest_email: str, db: Session = Depends(get_db)):
    db_guest = crud.get_guest_by_email(db=db, guest_email=guest_email)
    if db_guest is None:
        raise HTTPException(status_code=404, detail='This guest email does not exist.')
    return db_guest

@router.delete('/guests/id/{guest_id}/', status_code= status.HTTP_204_NO_CONTENT)
async def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    db_guest = crud.delete_guest(guest_id=guest_id, db= db)
    if db_guest is None:
        raise HTTPException(status_code=404, detail='This guest ID does not exist.')
    return

@router.delete('/guests/email/{guest_email}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_guest_email(guest_email: str, db: Session = Depends(get_db)):
    db_guest = crud.delete_guest_by_email(guest_email=guest_email, db=db)
    if not db_guest:
        raise HTTPException(status_code=404, detail='This email does not exist.')
    return

@router.patch('/guests/{guest_id}/', response_model=schemas.Guest)
async def patch_guest(guest_id: int, guest_update: schemas.GuestUpdate, db: Session = Depends(get_db)):
    db_guest = crud.patch_guest(db=db, guest_id=guest_id, guest_update=guest_update)
    if not db_guest:
        raise HTTPException(status_code=404, detail='This guest ID does not exist')
    return db_guest
