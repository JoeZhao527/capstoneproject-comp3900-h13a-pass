# crutial import for backend to run py itself
import os, sys

from sqlalchemy.orm import query
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server
from server import db
from backend.user_db import *
from backend.errors import *
from backend.data_access import create_schedule, get_eatery_id
from backend.user_db import *
from backend.voucher import *
from datetime import date, timedelta, time, datetime

# import schedule

weekdays = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
}

# function for deleting item in the database
def delete_item(item):
    db.session.delete(item)
    db.session.commit()


def add_schedule(token, eatery_id, no_vouchers, weekday, start, end, discount):
    start, end = convert_string_to_time(start), convert_string_to_time(end)
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # check weekday
    if weekday not in weekdays:
        raise InputError("Invalid weekday")
    # check time range
    if end <= start:
        raise InputError("End time cannot be before start time")
    
    # create schedule item and add into db
    schedule_id = create_schedule(eatery_id, no_vouchers, weekday, start, end, discount)
    
    # calculate the date for the voucher add this week or nxt week by given a weekday
    interval = date.today().weekday() - weekdays[weekday]
    # today's weekday is after the given weekday, add the voucher to the next weekday
    if interval > 0:
        voucher_date = date.today() - timedelta(abs(interval)) + timedelta(7)
    # weekday is equal to today's weekday, compare the time
    elif interval == 0:
        # if the voucher's end time is before the time now
        # add the voucher to next week
        if end <= datetime.now().time():
            voucher_date = date.today() - timedelta(abs(interval)) + timedelta(7)
        else:
            voucher_date = date.today() + timedelta(abs(interval))
    # today's weekday is before the given weekday, add the voucher on the weekday this week
    else:
        voucher_date = date.today() + timedelta(abs(interval))

    # Add vouchers with given voucher number
    for _ in range(int(no_vouchers)):
        add_voucher_by_schedule(eatery_id, voucher_date, start, end, discount, schedule_id)

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
# function for checking if the voucher is up to date by the schedule
def update_voucher_by_schedule():
    try:
        # loop through the schedule list, update this week's voucher by schedule one by one.
        schedules = Schedule.query.all()
        # check if the next 7 day's voucher is updated by this shedule
        for schedule in schedules:
            schedule_id = schedule.id
            weekday = schedule.weekday
            end = schedule.end_time
            # calculate the date for the voucher add this week or nxt week by given a weekday
            interval = date.today().weekday() - weekdays[weekday]
            # today's weekday is after the given weekday, add the voucher to the next weekday
            if interval > 0:
                voucher_date = date.today() - timedelta(abs(interval)) + timedelta(7)
            # weekday is equal to today's weekday, compare the time
            elif interval == 0:
                # if the voucher's end time is before the time now
                # add the voucher to next week
                if end <= datetime.now().time():
                    voucher_date = date.today() - timedelta(abs(interval)) + timedelta(7)
                else:
                    voucher_date = date.today() + timedelta(abs(interval))
            # today's weekday is before the given weekday, add the voucher on the weekday this week
            else:
                voucher_date = date.today() + timedelta(abs(interval))

            # check if these vouchers are already added into the database by this schedule
            # by given the schedule id and date
            voucher = Voucher.query.filter_by(schedule_id=schedule_id, date=voucher_date).first()
            # if there's no voucher added by this schedule of the next 7 days, then add them into the voucher database
            if not voucher:
                no_vouchers = schedule.no_vouchers
                eatery_id = schedule.eatery_id
                start = schedule.start_time
                end = schedule.end_time
                discount = schedule.discount
                for _ in range(int(no_vouchers)):
                    add_voucher_by_schedule(eatery_id, voucher_date, start, end, discount, schedule_id)
    except:
        print("update voucher failed")




# function for updating the schedule
def update_schedule(token, schedule_id, no_vouchers, weekday, start, end, discount):
    start, end = convert_string_to_time(start), convert_string_to_time(end)
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # check if the schedule id and eatery id is valid
    schedule =  Schedule.query.filter_by(id=schedule_id, eatery_id=eatery.id).first()
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

def voucher_has_expired(voucher):
    # to check if the voucher is after or equal to today's date
    if voucher.date < date.today():
        return True
    # now the date is good, check the end time
    else:
        # the voucher today is expired
        if voucher.date == date.today() and voucher.end_time <= datetime.now().time():
            return True
        # the voucher has not expired yet
        else: 
            return False

# function for removing the schedule
def remove_schedule(token, schedule_id):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # check if the schedule id is valid
    schedule = Schedule.query.filter_by(id=schedule_id, eatery_id=eatery.id).first()
    if schedule is None:
        raise InputError("Invalid schedule")

    # delete all the related voucher in the database
    vouchers = Voucher.query.filter_by(schedule_id=schedule_id).all()
    for voucher in vouchers:
        # if the voucher has not been booked and the voucher is future voucher, not expired yet
        if voucher.if_booked == False and not voucher_has_expired(voucher):
            delete_item(voucher)


    delete_item(schedule)
    return {}

# get all eatery's schedule by eatery's token
def get_eatery_schedule(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    schedule_list = []

    # get all the schedeule query
    # store the schedules into list
    for schedule in Schedule.query.filter_by(eatery_id=eatery.id).all():
        item = dict((col, getattr(schedule, col)) for col in schedule.__table__.columns.keys())
        # convert the start and end time to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        schedule_list.append(item)
    return { "schedules": schedule_list }

def convert_string_to_time(s):
    h, m = s.split(':')[0], s.split(':')[1]
    return time(int(h), int(m))

def convert_time_to_string(t):
    return str(t)[:-3]