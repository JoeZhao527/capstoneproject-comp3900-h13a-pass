# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *

# add and commit an item to database
def add_item(item):
    db.session.add(item)
    db.session.commit()

# delete and commit an item
def delete_item(item):
    db.session.delete(item)
    db.session.commit()

# insert an eatery to database
def create_eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, cuisine, city, suburb, description, token):
    eatery = Eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, cuisine, city, suburb, description, token)
    add_item(eatery)
    return eatery.id

def create_diner(first_name, last_name, email, password, phone, token):
    diner = Diner(first_name, last_name, email, password, phone, token)
    add_item(diner)
    return diner.id

# insert a Voucher to database
# useless function, the right one is in the voucher.py
#def create_Voucher(eatery_id, date, start_time, end_time, discount):
#    voucher = Voucher(eatery_id, date, start_time, end_time, discount)
#    add_item(voucher)
#    return voucher.id

# insert a schedule to database
def create_schedule(eatery_id, no_vouchers, weekday, start, end, discount):
    schedule = Schedule(eatery_id, no_vouchers, weekday, start, end, discount)
    add_item(schedule)
    return schedule.id

# insert a review to database
def create_review(diner_id, voucher_id, comment, rating):
    review = Review(diner_id, voucher_id, comment, rating)
    add_item(review)
    return review.id
# remove a review from database
def remove_review(review):
    delete_item(review)

# get eatery id by token
def get_eatery_id(token):
    eatery = Eatery.query.filter_by(token=token).first()
    return eatery.id

# get eatery information by id, for eatery public profile
def get_eatery_by_id(id):
    eatery = Eatery.query.filter_by(id=id).first()
    return dictionary_of_eatery(eatery)

# get eatery information by token for eatery profile
def get_eatery_by_token(token):
    eatery = Eatery.query.filter_by(token=token).first()
    return dictionary_of_eatery(eatery)

# get diner information by token for diner profile
def get_diner_by_token(token):
    diner = Diner.query.filter_by(token=token).first()
    data = dict((col, getattr(diner, col)) for col in diner.__table__.columns.keys())
    return data

# update user token
def update_eatery_token(token, eatery):
    eatery.token = token
    db.session.commit()

# upload an image
def store_image(eatery_id, image):
    img = Image(eatery_id, image)
    add_item(img)
    return img.id

def get_image(eatery_id):
    images = Image.query.filter_by(eatery_id=eatery_id).all()
    return [dict((col, getattr(img, col)) for col in img.__table__.columns.keys()) for img in images]

# get dictionary by given an eatery item (convert an eatery in database into a dictionary)
def dictionary_of_eatery(eatery):
    data = dict((col, getattr(eatery, col)) for col in eatery.__table__.columns.keys())
    return data
# get disctionary by given an diner item
def dictionary_of_diner(diner):
    data = dict((col, getattr(diner, col)) for col in diner.__table__.columns.keys())
    return data
# get dictionary of a voucher by given a voucher item
def dictionary_of_voucher(voucher):
    data = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
    return data
# get a list of all eateries
def get_all_eatery():
    eatery = Eatery.query.all()
    data = []
    for e in eatery:
        data.append(dictionary_of_eatery(e))
    return data

# function for generating a dictionary of city with it suburbs
"""
locations = {
    "Sydney" : ["Randwick", "Zetland"],
    "Melboune": [],
    "Brisbane": ["Bulwer"]
}
"""
def suburb_with_city():
    locations = {}
    eateries = Eatery.query.all()
    for eatery in eateries:
        city = eatery.city
        suburb = eatery.suburb
        # if this city already exist in the dictionary
        # just add the suburb into the suburb list of this city if the suburb is new
        if city in locations.keys():
            # if the suburb not exist in the list, add it
            if suburb not in locations[city]:
                locations[city].append(suburb)
        # if this city is not in the dictionary
        # create a empty suburb list for this city, then add the first suburb into the list
        else:
            locations[city] = []
            locations[city].append(suburb)
    return locations

# function for generating a list of cuisine of eatery
# return a list of cuisine from all the eateries
# ["chinese", "Japanese", "Korean", "Hotpot"] 
def cuisine_of_eateries():
    cuisine_list = []
    eateries = Eatery.query.all()
    for eatery in eateries:
        # each cuisine is a cuisine list separated by ','
        cuisines = eatery.cuisine.split(',')
        for cuisine in cuisines:
            # if this cuisine type not exist in the list
            if cuisine not in cuisine_list:
                cuisine_list.append(cuisine)
    return {'cuisine':cuisine_list}

