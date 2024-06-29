from pydantic import BaseModel
from datetime import date
from typing import Optional, Union

class PaymentBase(BaseModel):
    payment_date: date 
    payment_method: str 
    payment_status: str = 'Not paid'

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    payment_id: int
    booking_id: int 
    class Config:
        orm_mode=True

class PaymentUpdate(BaseModel):
    payment_date: date|None = None
    payment_method: str|None = None
    payment_status: str|None = None



class BookingBase(BaseModel):
    room_id: int
    check_in_date: date
    check_out_date: date

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    guest_id: int
    total_amount: float
    booking_status: str 
    
    class Config:
        orm_mode = True

class BookingUpdate(BaseModel):
    booking_status: str|None = None
    room_id: int|None = None
    check_in_date: date|None = None
    check_out_date: date|None = None



class GuestBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    date_of_birth: date

class GuestCreate(GuestBase):
    password: str

class Guest(GuestBase):
    reservations: list[Booking] = []
    class Config:
        orm_mode = True

class GuestUpdate(GuestBase):
    first_name: str|None = None
    last_name: str|None = None
    email: str|None = None
    password: str|None = None
    phone: str|None = None
    address: str|None = None
    date_of_birth: date|None = None




class RoomBase(BaseModel):
    room_type: str
    price_per_night: float
    availability_status: bool = True

class RoomCreate(RoomBase):
    pass 

class Room(RoomBase):
    room_id: int
    bookings: list[Booking] = []

    class Config:
        orm_mode = True

class RoomUpdate(BaseModel):
    room_type: str|None = None
    price_per_night: float|None = None
    availability_status: bool|None = None
    






