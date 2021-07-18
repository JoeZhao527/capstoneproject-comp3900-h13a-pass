# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.user_db import Eatery, Diner, Voucher, Image
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
def search_by_filter(date, time, location, cuisine):
    # search by date
    if date and not time and not location and not cuisine:
        # return a list of eatery objects pass the filter
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date).all()
    # search by time
    elif not date and time and not location and not cuisine:
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time).all()
    # search by location
    elif not date and not time and location and not cuisine:
        # a list to store eatery object that fit the location
        eateries = Eatery.query.all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    # search by cuisine
    elif not date and not time and not location and cuisine:
        result = Eatery.query.filter_by(cuisine=cuisine).all()
    # date and time
    elif date and time and not location and not cuisine:
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time).all()
    # date and location
    elif date and not time and location and not cuisine:
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    # date and cuisine
    elif date and not time and not location and cuisine:
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Eatery.cuisine == cuisine).all()
    # time and location
    elif not date and time and location and not cuisine:
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    # time and cuisine
    elif not date and time and not location and cuisine:
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time, Eatery.cuisine == cuisine).all()
    # location and cuisine
    elif not date and not time and location and cuisine:
        eateries = Eatery.query.filter_by(cuisine=cuisine).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    # date, time and location
    elif date and time and location and not cuisine:
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    # date, time and cuisine
    elif date and time and not location and cuisine:
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time, Eatery.cuisine == cuisine).all()
    # time, location and cuisine
    elif not date and time and location and cuisine:
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time, Eatery.cuisine == cuisine).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    # date, time, location and cuisine
    elif date and time and location and cuisine:
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time, Eatery.cuisine == cuisine).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    
    # if no date, time, location and cuisine speicify, return defalt -> a list of all the eateries
    else:
        result = Eatery.query.all()
    
    # conver the eateries object in the result to dictionary of eatery.
    # add the first image of the eatery into the dictionary
    # return a list of eateries with one image
    eatery_with_image = []
    for eat in result:
        eatery_item = dictionary_of_eatery(eat)
        # get the first image of the eatery
        first_image = Image.query.filter_by(eatery_id=eat.id).first()
        eatery_item["eatery_image"] = first_image.image if first_image else ''
        # add the eatery with image dictionary into the list
        eatery_with_image.append(eatery_item)

    return eatery_with_image
    #return [dictionary_of_eatery(eat) for eat in result]


# function for finding discount voucher based on given keyword
# key word use for matching the eatery_name
def search_by_key(keyword):
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
    # return [dictionary_of_eatery(eat) for eat in result]
    eateries = []
    for eat in result:
        eateries.append(dictionary_of_eatery(eat))
    return eateries

# function for viewing the eatery's profile by a given eatery id
def view_eatery_profile():
    return


# function for diner to book a voucher by given group id
def book_voucher(token, diner_id, group_id):
    # Check if given token of diner is valid
    if not valid_token(token):
        raise InputError("Invalid token")
    # Check if voucher(group id) exists
    voucher = Voucher.query.filter_by(group_id=group_id, if_booked=False).first()
    if voucher is None:
        raise InputError("Invalid voucher ID")
    # check if diner has booked the same group voucher already
    booked_same_voucher = Voucher.query.filter_by(group_id=group_id, diner_id=diner_id, if_booked=True).first()
    if booked_same_voucher:
        raise InputError("Diner has booked this voucher already!")
    # update the diner_id and if_booked in the voucher
    voucher.diner_id = diner_id
    voucher.if_booked = True
    db.session.commit()
    return {}
    
# function for cancelling a voucher by given a voucher id.
def cancel_voucher(token, diner_id, voucher_id):
    # Check if given token is valid
    if not valid_token(token):
        raise InputError("Invalid token")
    # Check if voucher exists
    voucher = Voucher.query.filter_by(id=voucher_id).first()
    if voucher is None:
        raise InputError("Voucher does not exist")
    # Check if the voucher is booked by this diner
    if voucher.diner_id != diner_id:
        raise InputError("Voucher is not booked by this diner")
    # update the info in this voucher
    voucher.diner_id = None
    voucher.if_booked = False
    db.session.commit()
    return {}

# show a list of eateries of this diners current or past bookings
def check_booking(token, diner_id):
    # List of bookings that diner has booked
    booking_list = []
    # for each voucher that matches this diners id, i.e. vouchers that this diner has booked
    # Create a dictionary object for each voucher and append to the list
    for voucher, eatery in db.session.query(Voucher, Eatery).join(Eatery, Voucher.eatery_id==Eatery.id).filter(Voucher.diner_id==diner_id).all():
        item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
        item["eatery_name"] = eatery.eatery_name
        item["eatery_phone"] = eatery.phone
        item["address"] = eatery.address + " " + eatery.suburb + " " + eatery.city
        item["cuisine"] = eatery.cuisine
        item["description"] = eatery.description
        item["menu"] = eatery.menu
        # convert the start and end time to string
        # convert the date to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        item['date'] = convert_date_to_string(item['date'])
        booking_list.append(item)
        
    return {booking_list}

# if time is not a string, conver it to a string
# if time is a string, return t
def convert_time_to_string(t):
    return str(t)[:-3] if not isinstance(t, str) else t

# if date is not a string, conver it to a string
# if date is a string, return date
def convert_date_to_string(d):
    return str(d) if not isinstance(d, str) else d

