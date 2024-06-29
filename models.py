#from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Guest(Base):
    __tablename__ = 'guests'

    guest_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String(50), unique=True)
    address = Column(String(50))
    date_of_birth = Column(Date)

    reservations = relationship('Booking', back_populates='guest', cascade='all, delete-orphan')
    


class Room(Base):
    __tablename__ = 'rooms'

    room_id = Column(Integer, primary_key=True)
    room_type = Column(String(20))
    price_per_night = Column(Float(10,2))
    availability_status = Column(Boolean)

    bookings = relationship('Booking', back_populates='room', cascade='all, delete-orphan')


class Booking(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey("guests.guest_id"))
    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    total_amount = Column(Float(10,2))
    booking_status = Column(String(20), default='pending')

    guest = relationship('Guest', back_populates='reservations')
    room = relationship('Room', back_populates='bookings')
    payment = relationship('Payment', uselist=False, back_populates='booking', cascade='all, delete-orphan')

class Payment(Base):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'), unique=True)
    payment_date = Column(Date)
    payment_method = Column(String(20))
    payment_status = Column(String(20))
   
    booking = relationship('Booking', back_populates='payment')

