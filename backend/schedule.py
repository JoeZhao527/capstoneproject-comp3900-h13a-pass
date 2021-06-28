# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server
from server import db
from .user_db import *
from backend.errors import *
from backend.data_access import create_Schedule
from backend.user_db import *

days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

def add_schedule(eatery_id, no_vouchers, weekday, start, end, discount, meal_type):
    # Checks discount 
    # Checks if a valid eatery_id
    # Checks if token is valid (decode)?
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    if not db.session.query(Eatery).filter_by(id=eatery_id).scalar():
        raise InputError("Eatery_id does not exist")
    if weekday not in days:
        raise InputError("Invalid weekday")
    if end <= start:
        raise InputError("End time cannot be before start time")
    
    schedule_id = create_Schedule(eatery_id, no_vouchers, weekday, start, end, discount, meal_type)
    return schedule_id

def update_schedule(token, weekday, start, end, discount, voucher_num, eatery_id, schedule_id):
    # Checks discount
    # Checks if token is valid
    # Checks if schedule and eatery id is valid
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    if not db.session.query(db.session.query(Schedule).filter_by(id=schedule_id, eatery_id=eatery_id)).scalar():
        raise InputError("No existing schedule_id for this eatery_id")
    if weekday not in days:
        raise InputError("Invalid weekday")
    if end <= start:
        raise InputError("End time cannot be before start time")
        
    schedule = Schedule.query.filter_by(eatery_id=eatery_id, weekday=weekday)
    schedule.voucher_num = voucher_num
    schedule.discount = discount
    schedule.start = start
    schedule.end = end
    db.session.commit()
    return {}


def remove_schedule(token, weekday, eatery_id, schedule_id):
    # If invalid schedule id
    if not db.session.query(db.session.query(Schedule).filter_by(id=schedule_id)).scalar():
        raise InputError("Invalid schedule")
    if weekday not in days:
        raise InputError("Invalid weekday")

    db.session.query(Schedule).filter_by(eatery_id=eatery_id, id=schedule_id).first().delete()
    db.session.commit()
    return {}
