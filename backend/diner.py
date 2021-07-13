# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.user_db import Eatery, Diner
from backend.errors import InputError
from server import db

# function for checking if the diner's token is valid
def valid_token(token):
    diner = Diner.query.filter_by(token=token).first()
    # diner = Diner.query.filter_by(token=token)
    if diner is None:
        return False
    return True

# function for finding (eateries) with discounts based on specified time range, location, or cuisine.
# maybe need postcode for eatery
def search_by_filter(token, date, start_time, end_time, location, cuisine):
    if not valid_token(token):
        raise InputError("Invalid token")
    # check if the start_time and end_time is invalid 

    # check if the start_time and end_time is valid

    # search by date
    if date and not location and not cuisine:
        
        
        return # list of eateries with a specific date
    # search by location
    elif not date and location and not cuisine:
        return # list of eateries with a specific location
    # search by cuisine
    elif not date and not location and cuisine:
        return # list of eateries with a specific location
    # time and location
    elif date and location and not cuisine:
        return # list of eateries with a specific date and location
    elif not date and location and cuisine:
        return #
    elif date and not location and cuisine:
        return #
    # time, location and cuisine type
    elif date and location and cuisine:
        return # list of eateries with specific date and location
    # if no date and no location and no cuisine speicify, return defalt
    return # list of all eateries
# function for finding discounts based on given keyword
def search_by_key(token, key):
    return
# function for viewing the eatery's location, menu, description and cuisines.
def view_eatery_list():
    return
# function for viewing the eatery's profile
def view_eatery_profile():
    return

# TODO: Sprint2 user story3
# function for booking a voucher
# 7. As a diner, I want to be able to book a voucher and see 
# the time range for the available discount voucher so that I 
# can plan ahead according to the booked voucher's time.
def book_voucher(token, diner_id, voucher_id):
    # Check if given token is valid
    if not valid_token(token):
        raise InputError("Invalid token")
    # Check if voucher exists
    voucher = Voucher.query.filter_by(id=voucher_id).first()
    if voucher is None:
        raise InputError("Voucher does not exist")
    # Get schedule information with voucher
    schedule = Schedule.query.filter_by(eatery_id=voucher.eatery_id, weekday=voucher.weekday, 
                                        start_time=voucher.start_time, end_time=voucher.end_time).first()
    # Check if schedule corresponds with this voucher
    if schedule is None:
        raise InputError("Schedule does not exist")
        
    voucher.diner_id = diner_id
    voucher.if_booked = true
    schedule.no_vouchers -= 1
    return {}
    
# function for cancelling a voucher.
def cancel_voucher(token, diner_id, voucher_id):
    # Check if given token is valid
    if not valid_token(token):
        raise InputError("Invalid token")
    # Check if voucher exists
    voucher = Voucher.query.filter_by(id=voucher_id).first()
    if voucher is None:
        raise InputError("Voucher does not exist")
    # Check if the voucher is booked by this diner
    if diner_id != voucher.diner_id:
        raise InputError("Voucher is not booked by this diner")
    # Get schedule information with voucher
    schedule = Schedule.query.filter_by(eatery_id=voucher.eatery_id, weekday=voucher.weekday, 
                                        start_time=voucher.start_time, end_time=voucher.end_time).first()
    # Check if schedule corresponds with this voucher
    if schedule is None:
        raise InputError("Schedule does not exist")
    
    voucher.diner_id = None
    voucher.if_booked = false
    schedule.no_voucher += 1;
    return {}

# TODO: Sprint2 user story4
# function for cheking the booked voucher and show the voucher code to the eatery
# given diner id, show a list of eateries that this diner has booked or is booking 
def check_booking(token, diner_id):
    booking_list = []
    # for voucher in Voucher.query.filter_by(diner_id=diner_id).all():
    #     booking_list.append(voucher.eatery_id)
    return { booking_list }# a list of eateries
