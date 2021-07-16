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
    eatery = Eatery.query.filter_by(id=eatery_id, token=token).first()
    # no eatery with given id or given token in the data
    if eatery is None:
        return False
    return True

# function for creating an voucher item and add into the voucher table
def create_voucher(eatery_id, date, start_time, end_time, discount, code, group_id):
    new_voucher = Voucher(eatery_id, date, start_time, end_time, discount, code, group_id)
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
    start, end = convert_string_to_time(start), convert_string_to_time(end)
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

    # check if the voucher already had a group
    voucher_group_id = db.session.query(Voucher.group_id).filter(Voucher.eatery_id == eatery_id, Voucher.date == date, Voucher.start_time == start, Voucher.end_time == end, Voucher.discount == discount).first()
    # if voucher does not belong to any of the group, generate a new group id
    if voucher_group_id is None:
        num_vouchers = len(Voucher.query.all())
        group_id = 1000 + num_vouchers
    # if voucher belongs to one of the group, add the group id
    else:
        group_id = voucher_group_id[0]
    # eatery and the other info are valid
    # create the voucher (convert the date into weekday)
    voucher = create_voucher(eatery_id, date, start, end, discount, code, group_id)
    voucher.if_used = False
    voucher.if_booked = False
    voucher.weekday = weekdays[date.weekday()] # datetime.datime.today().weekday()
    db.session.commit()

    return {'voucher_id': voucher.id, 'group_id': group_id}

# function for updating the voucher, date-> weekday, start time, end time, discount etc.
# not rlly got used, but if need to use, remember to update group id
def update_voucher(token, voucher_id, date, start, end, discount):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the token by the vouchr_id(eatery_id just in case)
    voucher = Voucher.query.filter_by(id=voucher_id, eatery_id=eatery.id).first()

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

# function for deleting the voucher by group_id
def delete_voucher_by_group(token, group_id):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the first voucher in the group and delete it
    voucher = Voucher.query.filter_by(group_id=group_id, eatery_id=eatery.id).first()
    delete_item(voucher)


# get all eatery's unbooked vouchers by eatery's token
def get_eatery_voucher(token):
    if type(token) == str:
        eatery = Eatery.query.filter_by(token=token).first()
    else:
        eatery = Eatery.query.filter_by(id=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []

    # get all the voucher query
    # store the unbooked vouchers into list
    for voucher in Voucher.query.filter_by(eatery_id=eatery.id, if_booked=False).all():
        item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
        # convert the start and end time to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        item['date'] = convert_date_to_string(item['date'])
        voucher_list.append(item)
    return {"vouchers": voucher_list}

# string type: "2014-06-08"     
def convert_string_to_date(s):
    if isinstance(s, str):
        y, m, d = s.split('-')[0], s.split('-')[1], s.split('-')[2]
        return date(int(y), int(m), int(d))
    return s

# string time type: "21:15"
def convert_string_to_time(s):
    if isinstance(s, str):
        h, m = s.split(':')[0], s.split(':')[1]
        return time(int(h), int(m))
    return s

# if time is not a string, conver it to a string
# if time is a string, return t
def convert_time_to_string(t):
    return str(t)[:-3] if not isinstance(t, str) else t

# if date is not a string, conver it to a string
# if date is a string, return date
def convert_date_to_string(d):
    return str(d) if not isinstance(d, str) else d

# for testing
if __name__ == "__main__":
    result1 = eatery_register("5678@gmail.com", "3936Cjj", "JJI", "ASSA", "04703977", "mR.cHEN", "HHHHH RAOD", "", "", "", "" ,"")
    result2 = add_voucher(result1["token"], result1["eatery_id"], "2021-07-17", "08:00", "10:00", 0.5)
    print(result2)
    result3 = add_voucher(result1["token"], result1["eatery_id"], "2021-07-17", "08:00", "10:00", 0.5)
    # print(result1)
    print(result3)

    result4 = add_voucher(result1["token"], result1["eatery_id"], "2021-07-17", "08:00", "10:00", 0.5)
    print(result4)

    result5 = add_voucher(result1["token"], result1["eatery_id"], "2021-08-17", "08:00", "10:00", 0.5)
    print(result5)

    result6 = add_voucher(result1["token"], result1["eatery_id"], "2021-08-17", "08:00", "10:00", 0.5)
    print(result6)

    check = get_eatery_voucher(result1["token"])
    print(check)
    
    delete_voucher_by_group(result1["token"], 1000)
    delete_voucher_by_group(result1["token"], 1000)
    check = get_eatery_voucher(result1["token"])
    print(check)