# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *

# add and commit an item to database
def add_item(item):
    db.session.add(item)
    db.session.commit()

# insert an eatery to database
def create_eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, cuisine, description, token):
    eatery = Eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, cuisine, description, token)
    add_item(eatery)
    return eatery.id

# insert a Voucher to database
def create_Voucher(eatery_id, date, start_time, end_time, discount):
    voucher = Voucher(eatery_id, date, start_time, end_time, discount)
    add_item(voucher)
    return voucher.id

# insert a schedule to database
def create_Schedule(eatery_id, no_vouchers, weekday, start, end, discount):
    schedule = Schedule(eatery_id, no_vouchers, weekday, start, end, discount)
    add_item(schedule)
    return schedule.id

# get eatery id by token
def get_eatery_id(token):
    eatery = Eatery.query.filter_by(token=token).first()
    return eatery.id

# get eatery information by id
def get_eatery_by_token(token):
    eatery = Eatery.query.filter_by(token=token).first()
    data = dict((col, getattr(eatery, col)) for col in eatery.__table__.columns.keys())
    return data

# update user token
def update_eatery_token(token, eatery):
    eatery.token = token
    db.session.commit()