# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server
from server import db
from backend.user_db import *
from backend.errors import *
from backend.data_access import create_Schedule
from backend.user_db import *
from backend.voucher import *
from datetime import date, timedelta
import schedule
import time

weekdays = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
}

# function for deleting item in the database
def delete_item(item):
    db.session.delete(item)
    db.session.commit()


def add_schedule(token, eatery_id, no_vouchers, weekday, start, end, discount):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token)
    if eatery is None:
        raise InputError("Invalid token")
    # check weekday
    if weekday not in weekdays:
        raise InputError("Invalid weekday")
    # check time range
    if end <= start:
        raise InputError("End time cannot be before start time")
    # checks discount
    if discount > 1:
        raise InputError("Discount cannot be greater than 1")
    
    # create schedule item and add into db
    schedule_id = create_Schedule(eatery_id, no_vouchers, weekday, start, end, discount)
    
    # calculate the date for the voucher add this week or nxt week by given a weekday
    interval = date.today().weekday - weekdays[weekday]
    # today's weekday is after the given weekday, add the voucher to the next weekday
    if interval > 0:
        voucher_date = date.today() - timedelta(abs(interval)) + timedelta(7)
    # today's weekday is before or on the given weekday, add the voucher on the weekday this week
    else:
        voucher_date = date.today() + timedelta(abs(interval))

    # Add vouchers with given voucher number
    for _ in range(no_vouchers):
        add_voucher(token, voucher_date, start, end, discount, eatery_id)

    return {'schedule_id': schedule_id}

"""
def add_voucher_by_schedule(token, eatery_id, no_vouchers, weekday, start, end, discount):
    # if the vouchers for a weekday this week(specific date) are already added, do nothing
    # else add vouchers with given voucher num
    voucher = Voucher.query.filter_by(eatery_id=eatery_id, date=date)
    if voucher is None:
        for _ in range(no_vouchers):
            add_voucher(token, date, start, end, discount, eatery_id)

schedule.every(10).minutes.do(add_voucher_by_schedule)
while True:
    schedule.run_pending(add_voucher_by_schedule())
    time.sleep(1)
"""

# function for updating the schedule
def update_schedule(token, schedule_id, no_vouchers, weekday, start, end, discount):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token)
    if eatery is None:
        raise InputError("Invalid token")
    # check if the schedule id and eatery id is valid
    schedule =  Schedule.query.filter_by(id=schedule_id, eatery_id=eatery.id)
    if schedule is None:
        raise InputError("No existing schedule_id for this eatery_id")
    # check weekday
    if weekday not in weekdays:
        raise InputError("Invalid weekday")
    # check time range
    if end <= start:
        raise InputError("End time cannot be before start time")
    # checks discount
    if discount > 1:
        raise InputError("Discount cannot be greater than 1")
        
    # schedule = Schedule.query.filter_by(id=schedule_id, eatery_id=eatery.id)
    schedule.no_voucher = no_vouchers
    schedule.weekday = weekday
    schedule.start = start
    schedule.end = end
    schedule.discount = discount
    db.session.commit()
    return {}

# function for removing the schedule
def remove_schedule(token, schedule_id):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token)
    if eatery is None:
        raise InputError("Invalid token")
    # check if the schedule id is valid
    schedule = Schedule.query.filter_by(id=schedule_id, eatery_id=eatery.id)
    if schedule is None:
        raise InputError("Invalid schedule")

    delete_item(schedule)
    return {}

#if __name__ == "__main__":
    