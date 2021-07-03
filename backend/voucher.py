# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.auth import *
from backend.user_db import *

from datetime import date, datetime
from server import db
import string
import random

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
def add_voucher(token, date, start, end, discount, eatery_id):
    # check if eatery is valid by check the eatery id and token
    if not valid_eatery(eatery_id, token):
        raise InputError("Invalid token")
    # check if the voucher date and time is valid
    if date < date.today() or (date == date.today() and end < datetime.now()):
        raise InputError("Voucher Time invalid")
    
    # creating a radom verify code for eatery and user to cehck the voucher
    mix = string.ascii_letters + string.digits
    code = ''.join(random.choice(mix) for i in range(20))

    # eatery and the other info are valid
    # create the voucher (convert the date into weekday)
    voucher = create_voucher(eatery_id, date, start, end, discount, code)
    voucher.if_used = False
    voucher.if_booked = False
    voucher.weekday = date.weekday() # datetime.datime.today().weekday()
    db.session.commit()

    return {'voucher_id': voucher.id}

# function for updating the voucher, date-> weekday, start time, end time, discount etc.
def update_voucher(token, voucher_id, date, start, end, discount):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token)
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
    eatery = Eatery.query.filter_by(token=token)
    if eatery is None:
        raise InputError("Invalid token")
    # get the voucher and delete it 
    voucher = Voucher.query.filter_by(id=voucher_id, eatery_id=eatery.id)
    delete_item(voucher)







