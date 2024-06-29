from .. import models, schemas
from .. import crud
from ..get_db import get_db
from sqlalchemy.orm import Session
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter()

@router.post('/rooms/{room_id}/', response_model=schemas.Room)
async def create_room(room_id: int, room : schemas.RoomCreate, db: Session = Depends(get_db)):
    if crud.get_room(db=db, room_id=room_id):
        raise HTTPException(status_code=400, detail='Room already created.')
    
    return crud.create_room(db= db, room =room, room_id=room_id)

@router.get('/rooms/', response_model=list[schemas.Room])
async def read_all_rooms(db: Session = Depends(get_db)):
    return crud.get_all_rooms(db=db)

@router.get('/rooms/{room_id}/', response_model=schemas.Room)
async def read_rooms(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room(db = db, room_id=room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail='This room ID does not exist.')
    return db_room

@router.delete('/rooms/{room_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.delete_room(db=db, room_id=room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail='This room ID does not exist.')
    return

@router.patch('/rooms/{room_id}/', response_model= schemas.Room)
async def patch_room(room_id: int, room_update: schemas.RoomUpdate, db: Session = Depends(get_db)):
    db_room = crud.patch_room(db=db, room_id=room_id, room_update=room_update)
    if not db_room:
        raise HTTPException(status_code=404, detail='This room ID does not exist.')
    return db_room

@router.get('/free_rooms/', response_model=list[schemas.Room])
async def get_free_rooms(check_in_date: date, check_out_date: date, db: Session = Depends(get_db)):
    db_free_rooms = crud.get_free_rooms(db=db, check_in_date=check_in_date, check_out_date=check_out_date)
    if not db_free_rooms:
        raise HTTPException(status_code=404, detail='There are no available rooms for this period.')
    return db_free_rooms