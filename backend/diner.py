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

# function for booking a voucher
def book_voucher(token, diner_id, voucher_id):
    # Check if given token of diner is valid
    if not valid_token(token):
        raise InputError("Invalid token")
    # Check if voucher exists
    voucher = Voucher.query.filter_by(id=voucher_id).first()
    if voucher is None:
        raise InputError("Voucher does not exist")

    voucher.diner_id = diner_id
    voucher.if_booked = true
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

    voucher.diner_id = None
    voucher.if_booked = false
    return {}

# Shows a list of eateries of this diners current or past bookings
def check_booking(token, diner_id):
    # List of bookings that diner has booked
    booking_list = []
    # for each voucher that matches this diners id, i.e. vouchers that this diner has booked
    # Create a dictionary object for each voucher and append to the list
    for voucher, eatery_name in db.session.query(Voucher, Eatery.eatery_name).join(Eatery, Voucher.eatery_id==Eatery.id).filter(Voucher.diner_id==diner_id).all():
        item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
        item["eatery_name"] = eatery_name
        # convert the start and end time to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        booking_list.append(item)
        
    return { booking_list }

def convert_time_to_string(t):
    return str(t)[:-3]