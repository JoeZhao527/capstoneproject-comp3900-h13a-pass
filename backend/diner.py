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
def book_voucher(token, diner_id, voucher_id):
    return
# function for cancelling a voucher.
def cancel_voucher(token, diner_id, voucher_id):
    return

# TODO: Sprint2 user story4
# function for cheking the booked voucher and show the voucher code to the eatery
# given diner id, show a list of eateries that this diner has booked or is booking 
def check_booking(token, diner_id):
    return # a list of eateries
