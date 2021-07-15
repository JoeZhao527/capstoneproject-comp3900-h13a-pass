# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.user_db import Eatery, Diner, Voucher
from backend.data_access import dictionary_of_eatery
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
# location = suburb(postcode)
def search_by_filter(token, date, time, location, cuisine):
    if not valid_token(token):
        raise InputError("Invalid token")
    # search by date
    if date and not time and not location and not cuisine:
        # return a list of eatery objects pass the filter
        result = Eatery.query.join(Voucher).filter(Voucher.date == date).all()
    # search by time
    elif not date and time and not location and not cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.start_time <= time, Voucher.end_time >= time).all()
    # search by location
    elif not date and not time and location and not cuisine:
        result = Eatery.query.filter_by(suburb=location).all()
    # search by cuisine
    elif not date and not time and not location and cuisine:
        result = Eatery.query.filter_by(cuisine=cuisine).all()
    # date and time
    elif date and time and not location and not cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time).all()
    # date and location
    elif date and not time and location and not cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.date == date, Eatery.suburb == location).all()
    # date and cuisine
    elif date and not time and not location and cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.date == date, Eatery.cuisine == cuisine).all()
    # time and location
    elif not date and time and location and not cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.start_time <= time, Voucher.end_time >= time, Eatery.suburb == location).all()
    # time and cuisine
    elif not date and time and not location and cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.start_time <= time, Voucher.end_time >= time, Eatery.cuisine == cuisine).all()
    # location and cuisine
    elif not date and not time and location and cuisine:
        result = Eatery.query.filter_by(suburb=location, cuisine=cuisine).all()
    # date, time and location
    elif date and time and location and not cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time, Eatery.suburb == location).all()
    # date, time and cuisine
    elif date and time and not location and cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time, Eatery.cuisine == cuisine).all()
    # time, location and cuisine
    elif not date and time and location and cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.start_time <= time, Voucher.end_time >= time, Eatery.suburb == location, Eatery.cuisine == cuisine).all()
    elif date and time and location and cuisine:
        result = Eatery.query.join(Voucher).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time, Eatery.suburb == location, Eatery.cuisine == cuisine).all()
    # if no date, time, location and cuisine speicify, return defalt -> a list of all the eateries
    else:
        result = Eatery.query.all()
    
    # conver the eateries object in the result to dictionary of eatery.
    # return a list of eateries
    eateries = []
    for eat in result:
        eateries.append(dictionary_of_eatery(eat))
    return eateries


# function for finding discount voucher based on given keyword
# key word use for matching the eatery_name
def search_by_key(token, keyword):
    if not valid_token(token):
        raise InputError("Invalid token")
    result = Eatery.query.all()
    eateries = []
    
    # for all the eateries objects in the database
    for eat in result:
        # if keyword match the eatery_name
        if (keyword in eat.eatery_name):
            eateries.append(dictionary_of_eatery(eat))
    return eateries

# function for viewing the eatery's location, menu, description and cuisines.
# just return a list of eateries
# maybe can make it more specific later
def view_eatery_list():
    result = Eatery.query.all()
    eateries = []
    for eat in result:
        eateries.append(dictionary_of_eatery(eat))
    return eateries

# function for viewing the eatery's profile by a given eatery id
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
    return # a list of
