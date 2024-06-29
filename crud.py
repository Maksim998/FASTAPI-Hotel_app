from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt
from datetime import date


async def get_price_per_night(room_id: int, db: Session):
    return db.query(models.Room).filter(models.Room.room_id == room_id).first().price_per_night

async def get_all_guests(db:Session):
    return db.query(models.Guest).all()

async def get_guest(db: Session, guest_id: int):
    return db.query(models.Guest).filter(models.Guest.guest_id == guest_id).first()

async def get_guest_by_email(db: Session, guest_email: str):
    return db.query(models.Guest).filter(models.Guest.email == guest_email).first()

async def get_all_rooms(db:Session):
    return db.query(models.Room).all()

async def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.room_id == room_id). first()

async def is_room_reserved(db: Session, room_id: int, check_in_date: date, check_out_date: date):
   
    return db.query(models.Booking).filter(
    (models.Booking.room_id == room_id) &
    (
        (models.Booking.check_in_date <= check_in_date) &
        (models.Booking.check_out_date >= check_in_date) |
        (models.Booking.check_in_date <= check_out_date) &
        (models.Booking.check_out_date >= check_out_date) |
        (models.Booking.check_in_date >= check_in_date) &
        (models.Booking.check_out_date <= check_out_date)
        )
    ).first()
    
async def get_free_rooms(db:Session, check_in_date: date, check_out_date: date):
    subquery =  db.query(models.Booking.room_id).filter((
        (models.Booking.check_in_date <= check_in_date) &
        (models.Booking.check_out_date >= check_in_date) |
        (models.Booking.check_in_date <= check_out_date) &
        (models.Booking.check_out_date >= check_out_date) |
        (models.Booking.check_in_date >= check_in_date) &
        (models.Booking.check_out_date <= check_out_date)
        )).subquery()
    return db.query(models.Room).filter(models.Room.room_id.notin_(subquery)).all()

async def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()

async def get_all_bookings_by_room(db: Session, room_id: int):
    return db.query(models.Booking).filter(models.Booking.room_id == room_id).all()

async def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()

async def get_payment_by_booking_id(db: Session, booking_id: int):
    return db.query(models.Payment).filter(models.Payment.booking_id == booking_id).first()

async def create_guest(db: Session, guest: schemas.GuestCreate):

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(guest.password.encode('utf-8'), salt)

    guest_dict = guest.model_dump()
    guest_dict.pop('password')
    db_guest = models.Guest(**guest_dict, hashed_password = hashed_password.decode('utf-8'))
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

async def create_room(db: Session, room_id: int, room: schemas.RoomCreate):
    
    db_room = models.Room(**room.model_dump(), room_id = room_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

async def create_booking(db: Session, booking: schemas.BookingCreate, guest_id:int, price_per_night: float):
    
    db_booking = models.Booking(**booking.model_dump(), guest_id=guest_id, total_amount = (booking.check_out_date - booking.check_in_date).days*price_per_night)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking

async def create_payment(db: Session, payment: schemas.PaymentCreate, booking_id: int):

    db_payment = models.Payment(**payment.model_dump(), booking_id = booking_id)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


async def delete_guest(db: Session, guest_id: int):
    db_guest = db.query(models.Guest).filter(models.Guest.guest_id == guest_id).first()
    if not db_guest:
        return None
    db.delete(db_guest)
    db.commit()
    return db_guest
    
    
async def delete_guest_by_email(db: Session, guest_email: str):
    db_guest = db.query(models.Guest).filter(models.Guest.email == guest_email).first()
    if not db_guest:
        return None
    db.delete(db_guest)
    db.commit()
    return db_guest


async def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if not db_room:
        return None
    db.delete(db_room)
    db.commit()
    print(db_room)
    return db_room


async def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not db_booking:
        return None
    db.delete(db_booking)
    db.commit()
    return db_booking


async def delete_payment(db: Session, payment_id: int):
    db_payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
    if not db_payment:
        return None
    db.delete(db_payment)
    db.commit()
    return db_payment


async def patch_guest(db: Session, guest_id:int, guest_update: schemas.GuestUpdate):
    db_guest = get_guest(db=db, guest_id=guest_id)
    if not db_guest:
        return None
    
    for key, val in guest_update.model_dump(exclude_unset= True).items():
        
        if val != None:
            if key == 'password':
                salt = bcrypt.gensalt()
                print(val)
                hashed_password = bcrypt.hashpw(val.encode('utf-8'), salt).decode('utf-8')
                print(hashed_password)
                setattr(db_guest, 'hashed_password', hashed_password)
            
            else:
                setattr(db_guest, key, val)
            

    db.commit()
    db.refresh(db_guest)
    return db_guest

async def patch_room( db: Session, room_id: int, room_update: schemas.RoomUpdate):
    db_room = get_room(db=db, room_id=room_id)
    if not db_room:
        return None
    
    for key, val in room_update.model_dump(exclude_unset=True).items():
        
        if val != None:
            setattr(db_room, key, val)

    db.commit()
    db.refresh(db_room)
    return db_room

async def patch_booking(db: Session, booking_id: int, booking_update: schemas.BookingUpdate):
    db_booking = get_booking(db=db, booking_id=booking_id)
    if not db_booking:
        return None
    
    for key, val in booking_update.model_dump(exclude_unset=True).items():

        if val != None:
            setattr(db_booking, key, val)
    

    db.commit()
    db.refresh(db_booking)
    return db_booking

async def patch_payment(db: Session, payment_id: int, payment_update: schemas.PaymentUpdate):
    db_payment = get_payment(db=db, payment_id=payment_id)
    if not db_payment:
        return None
    
    for key,val in payment_update.model_dump(exclude_unset=True).items():

        if val != None:
            setattr(db_payment, key, val)

        db.commit()
        db.refresh(db_payment)
        return db_payment


