from . import models, schemas, crud
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException
from .Routers import guest, room, booking, payment

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(guest.router)
app.include_router(room.router)
app.include_router(booking.router)
app.include_router(payment.router)