# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.auth import *
from backend.user_db import *

from datetime import date, datetime, time
from server import db
import string
import random

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# function for cheking valid eatery
def valid_eatery(eatery_id, token):
    eatery = Eatery.query.filter_by(id=eatery_id, token=token)
    # no eatery with given id or given token in the data
    if eatery is None:
        return False
    return True

# function for creating an voucher item and add into the voucher table
def create_voucher(eatery_id, date, start_time, end_time, discount, code):
    new_voucher = Voucher(eatery_id, date, start_time, end_time, discount, code)
    add_item(new_voucher)
    return new_voucher


# function for adding item in the database
def add_item(item):
    db.session.add(item)
    db.session.commit()

# function for deleting item in the database
def delete_item(item):
    db.session.delete(item)
    db.session.commit()

# function for generating voucher
def add_voucher(token, eatery_id, date, start, end, discount):
    start, end = convert_time(start), convert_time(end)
    date = convert_string_to_date(date)
    # check if eatery is valid by check the eatery id and token
    if not valid_eatery(eatery_id, token):
        raise InputError("Invalid token")
    # check if the voucher date and time is valid
    if date < date.today() or (date == date.today() and end < datetime.now().time()):
        raise InputError("Voucher Time invalid")
    
    # creating a radom verify code for eatery and user to cehck the voucher
    mix = string.ascii_letters + string.digits
    code = ''.join(random.choice(mix) for i in range(20))

    # eatery and the other info are valid
    # create the voucher (convert the date into weekday)
    voucher = create_voucher(eatery_id, date, start, end, discount, code)
    voucher.if_used = False
    voucher.if_booked = False
    voucher.weekday = weekdays[date.weekday()] # datetime.datime.today().weekday()
    db.session.commit()

    return {'voucher_id': voucher.id}

# function for updating the voucher, date-> weekday, start time, end time, discount etc.
def update_voucher(token, voucher_id, date, start, end, discount):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the token by the vouchr_id(eatery_id just in case)
    voucher = Voucher.query.filter_by(id=voucher_id, eatery_id=eatery.id)

    voucher.date = date
    voucher.start = start
    voucher.end = end
    voucher.discount = discount
    voucher.weekday = date.weekday() # datetime.datime.today().weekday()
    db.session.commit()



# function for deleting the voucher
def delete_voucher(token, voucher_id):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the voucher and delete it 
    voucher = Voucher.query.filter_by(id=voucher_id, eatery_id=eatery.id).first()
    delete_item(voucher)

# get all eatery's vouchers by eatery's token
def get_eatery_voucher(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []

    # get all the schedeule query
    # store the schedules into list
    for voucher in Voucher.query.filter_by(eatery_id=eatery.id).all():
        item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
        # convert the start and end time to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        item['date'] = convert_date_to_string(item['date'])
        voucher_list.append(item)
    return { "vouchers": voucher_list }

def convert_string_to_date(s):
    if isinstance(s, str):
        y, m, d = s.split('-')[0], s.split('-')[1], s.split('-')[2]
        return date(int(y), int(m), int(d))
    return s

def convert_time(s):
    if isinstance(s, str):
        h, m = s.split(':')[0], s.split(':')[1]
        return time(int(h), int(m))
    return s

def convert_time_to_string(t):
    return str(t)[:-3] if not isinstance(t, str) else t

def convert_date_to_string(d):
    return str(d) if not isinstance(d, str) else d