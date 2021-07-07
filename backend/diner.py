# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.user_db import Eatery, Diner
from backend.errors import InputError
from server import db

# function for checking if the diner's token is valid
def valid_token(token):
    diner = Diner.query.filter_by(token=token)
    # diner = Diner.query.filter_by(token=token)
    if diner is None:
        return False
    return True

# function for finding discounts based on specified time range, location, or cuisine.
def search_by_filter(token, date, location, cuisine):
    if not valid_token(token):
        raise InputError("Invalid token")
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