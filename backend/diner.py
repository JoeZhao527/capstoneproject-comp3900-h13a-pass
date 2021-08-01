# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.user_db import Eatery, Diner, Voucher, Image, Review
from backend.data_access import dictionary_of_eatery, create_review, remove_review
from backend.errors import InputError
from server import db
from datetime import date, datetime, time

# function for checking if the diner's token is valid
def valid_token(token):
    diner = Diner.query.filter_by(token=token).first()
    # diner = Diner.query.filter_by(token=token)
    if diner is None:
        return False
    return True

# function for getting today's date, for search_by_filter only
def get_date_today():
    return date.today()

# function for getting now's time
def get_time_now():
    return datetime.now().time()

# function for finding (eateries) with discounts based on specified time range, location, or cuisine.
# maybe need postcode for eatery
# location = suburb(postcode)
def search_by_filter(date, time, location, cuisine):
    # conver date and time (string) to date and time(date and time type)
    date = convert_string_to_date(date)
    time = convert_string_to_time(time)
    
    # search by date
    if date and not time and not location and not cuisine:
        # return a list of eatery objects pass the filter
        eateries = db.session.query(Eatery, Voucher).join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date).all()
        result = []
        for eatery, voucher in eateries:
            # compare the voucher's time to the time now
            if not voucher_has_expired(voucher):
                result.append(eatery)
    # search by time
    elif not date and time and not location and not cuisine:
        date_today = get_date_today()
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time, Voucher.date >= date_today).all()
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
        eateries = Eatery.query.all()
        result = []
        for eatery in eateries:
            # cuisine = "Chinese",  eatery.cuisine = "Chinese, Hotpot"
            if cuisine in eatery.cuisine:
                result.append(eatery)
    # date and time
    elif date and time and not location and not cuisine:
        result = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time).all()
    # date and location
    elif date and not time and location and not cuisine:
        eateries = db.session.query(Eatery, Voucher).join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date).all()
        result = []
        for eatery, voucher in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # compare the voucher's time to the time now
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if not voucher_has_expired(voucher) and location in eat_location:
                result.append(eatery)
    # date and cuisine
    elif date and not time and not location and cuisine:
        eateries = db.session.query(Eatery, Voucher).join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date).all()
        result = []
        for eatery, voucher in eateries:
            # cuisine = "Chinese",  eatery.cuisine = "Chinese, Hotpot"
            if not voucher_has_expired(voucher) and cuisine in eatery.cuisine:
                result.append(eatery)
    # time and location
    elif not date and time and location and not cuisine:
        date_today = get_date_today()
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time, Voucher.date >= date_today).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location:
                result.append(eatery)
    # time and cuisine
    elif not date and time and not location and cuisine:
        date_today = get_date_today()
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time, Voucher.date >= date_today).all()
        result = []
        for eatery in eateries:
            # cuisine = "Chinese",  eatery.cuisine = "Chinese, Hotpot"
            if cuisine in eatery.cuisine:
                result.append(eatery)
    # location and cuisine
    elif not date and not time and location and cuisine:
        eateries = Eatery.query.all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            eat_location = eatery.city + "," + eatery.suburb
            eat_cuisine = eatery.cuisine
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            if location in eat_location and cuisine in eat_cuisine:
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
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time).all()
        result = []
        for eatery in eateries:
            # cuisine = "Chinese",  eatery.cuisine = "Chinese, Hotpot"
            if cuisine in eatery.cuisine:
                result.append(eatery)
    # date, location and cuisine
    elif date and not time and location and cuisine:
        eateries = db.session.query(Eatery, Voucher).join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date).all()
        result = []
        for eatery, voucher in eateries:
            # eat_location would be "Sydney,Randwick"
            # eat_cuisine would be "Chinese, Hotpot"
            eat_location = eatery.city + "," + eatery.suburb
            eat_cuisine = eatery.cuisine
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            # cuisine could be "Chinese", "Hotpot", "Chinese, hotpot"
            if not voucher_has_expired(voucher) and location in eat_location and cuisine in eat_cuisine:
                result.append(eatery)
    
    # time, location and cuisine
    elif not date and time and location and cuisine:
        date_today = get_date_today()
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.start_time <= time, Voucher.end_time >= time, Voucher.date >= date_today).all()
        result = []
        for eatery in eateries:
            # eat_location would be "Sydney,Randwick"
            # eat_cuisine would be "Chinese, Hotpot"
            eat_location = eatery.city + "," + eatery.suburb
            eat_cuisine = eatery.cuisine
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            # cuisine could be "Chinese", "Hotpot", "Chinese, hotpot"
            if location in eat_location and cuisine in eat_cuisine:
                result.append(eatery)
    # date, time, location and cuisine
    elif date and time and location and cuisine:
        eateries = Eatery.query.join(Voucher, Voucher.eatery_id==Eatery.id).filter(Voucher.date == date, Voucher.start_time <= time, Voucher.end_time >= time).all()
        result = []
        for eatery in eateries:
            # eat_location could be "Sydney,Randwick"
            # eat_cuisine could be "Chinese, Hotpot"
            eat_location = eatery.city + "," + eatery.suburb
            eat_cuisine = eatery.cuisine
            # location could be "Sydney", "Randwick", "Sydney,Randwick"
            # cuisine could be "Chinese", "Hotpot", "Chinese, hotpot"
            if location in eat_location and cuisine in eat_cuisine:
                result.append(eatery)
    
    # if no date, time, location and cuisine speicify, return defalt -> a list of all the eateries
    else:
        result = Eatery.query.all()
    
    # conver the eateries object in the result to dictionary of eatery.
    # add the first image of the eatery into the dictionary
    # return a list of eateries with one image
    eatery_image_review = []

    # make the eatery object in the result disctinct
    result = list(set(result))
    for eat in result:
        eatery_item = dictionary_of_eatery(eat)
        # get the first image of the eatery
        first_image = Image.query.filter_by(eatery_id=eat.id).first()
        eatery_item["eatery_image"] = first_image.image if first_image else ''

        num_of_review, avg_rating = avg_review(eat.id)

        eatery_item["num_of_review"] = num_of_review
        eatery_item["avg_rating"] = avg_rating

        # add the eatery with image dictionary into the list
        # if the eatery_item is alreayd in the list, do not append it
        eatery_image_review.append(eatery_item)

    return eatery_image_review
    #return [dictionary_of_eatery(eat) for eat in result]


# function for finding discount voucher based on given keyword
# key word use for matching the eatery_name
def search_by_key(keyword):
    result = Eatery.query.all()
    eateries = []
    # for all the eateries objects in the database
    for eat in result:
        # if keyword match the eatery_name
        if (keyword.lower() in eat.eatery_name.lower()):
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
# (updated) also diner will be asked to add in arrival info: arrival time, num, and special request when they complete the booking
def book_voucher(token, group_id, arrival_time, num_of_guest, special_request):
    diner = Diner.query.filter_by(token=token).first()
    # Check if given token is valid
    if diner is None:
        raise InputError("Invalid token")
    # Check if voucher(group id) exists
    voucher = Voucher.query.filter_by(group_id=group_id, if_booked=False).first()
    if voucher is None:
        raise InputError("Invalid voucher ID")
    # check if diner has booked the same group voucher already
    booked_same_voucher = Voucher.query.filter_by(group_id=group_id, diner_id=diner.id, if_booked=True).first()
    if booked_same_voucher:
        raise InputError("Diner has booked this voucher already!")
    # update the diner_id and if_booked in the voucher
    voucher.diner_id = diner.id
    voucher.if_booked = True
    voucher.arrival_time = convert_string_to_time(arrival_time)
    voucher.num_of_guest = num_of_guest
    voucher.special_request = special_request
    db.session.commit()
    return {}
    
# function for cancell booking a voucher by given a voucher id.
# (updated)
def cancel_voucher(token, voucher_id):
    diner = Diner.query.filter_by(token=token).first()
    # Check if given token is valid
    if diner is None:
        raise InputError("Invalid token")
    # Check if voucher exists, booked and not used
    voucher = Voucher.query.filter_by(id=voucher_id, if_booked=True, if_used=False).first()
    if voucher is None:
        raise InputError("Voucher does not exist")
    # Check if the voucher is booked by this diner
    if voucher.diner_id != diner.id:
        raise InputError("Voucher is not booked by this diner")
    # update the info in this voucher
    voucher.diner_id = None
    voucher.if_booked = False
    voucher.arrival_time = None
    voucher.num_of_guest = None
    voucher.special_request = None

    db.session.commit()
    return {}
   
"""
# show a list of eateries of this diners current or past bookings
# (did any frontend use this function?)
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
        # convert the start and end time and arrival time to string
        # convert the date to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        item['arrival_time'] = convert_time_to_string(item['arrival_time'])
        item['date'] = convert_date_to_string(item['date'])
        booking_list.append(item)
        
    return {booking_list}
"""

# function for checking if a voucher has expired or not
# by given a voucher item, check if this voucher has expired
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

# get diner's booked vouchers by diner's token
# 1. booked, not used and not expired (available)
# (updated the arrival time)
def get_booked_voucher(token):
    diner = Diner.query.filter_by(token=token).first()
    # check if diner exist
    if diner is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are booked, not used and not expired by this diner
    # with the related eatery
    voucher_eatery_list = db.session.query(Voucher, Eatery).join(Eatery, Voucher.eatery_id==Eatery.id).filter(Voucher.diner_id==diner.id, Voucher.if_booked==True, Voucher.if_used==False).all()
    for voucher, eatery in voucher_eatery_list:
        # and the voucher has not expired        
        if not voucher_has_expired(voucher):
            item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
            # convert the start and end time to string
            item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
            item['date'] = convert_date_to_string(item['date'])
            # conver the arrival time to string
            item['arrival_time'] = convert_time_to_string(item['arrival_time'])
            
            # also add the information of related eatery
            item["eatery_name"] = eatery.eatery_name
            item["eatery_phone"] = eatery.phone

            # the voucher must not be expired in this list
            # this is a temporary solution, propery way should be having a expired attribute in voucher
            item['expired'] = False
            voucher_list.append(item)
    # return {"vouchers": voucher_list}
    return {"vouchers": voucher_list}


# get diner's booked and used vouchers by diner's token
# 2. booked and used (not available)
# (updated the arrival time)
def get_used_voucher(token):
    diner = Diner.query.filter_by(token=token).first()
    # check if diner exist
    if diner is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are booked and used(whatever expired or not)by this diner
    voucher_eatery_list = db.session.query(Voucher, Eatery).join(Eatery, Voucher.eatery_id==Eatery.id).filter(Voucher.diner_id==diner.id, Voucher.if_booked==True, Voucher.if_used==True).all()
    for voucher, eatery in voucher_eatery_list:
        item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
        # convert the start and end time to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        item['date'] = convert_date_to_string(item['date'])
        
        # conver the arrival time to string
        item['arrival_time'] = convert_time_to_string(item['arrival_time'])
        
        # also add the information of related eatery
        item["eatery_name"] = eatery.eatery_name
        item["eatery_phone"] = eatery.phone
        voucher_list.append(item)
    
    return {"vouchers": voucher_list}

# this collide with get_booked_expired_voucher in voucher.py
# get diner's booked, not used but expired vouchers by diner's token
# 3. booked, not used and expired (not available)
def diner_get_booked_expired_voucher(token):
    diner = Diner.query.filter_by(token=token).first()
    # check if diner exist
    if diner is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are booked, not used by this diner
    voucher_eatery_list = db.session.query(Voucher, Eatery).join(Eatery, Voucher.eatery_id==Eatery.id).filter(Voucher.diner_id==diner.id, Voucher.if_booked==True, Voucher.if_used==False).all()
    for voucher, eatery in voucher_eatery_list:
        # and the voucher has expired        
        if voucher_has_expired(voucher):
            item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
            # convert the start and end time to string
            item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
            item['date'] = convert_date_to_string(item['date'])

            # conver the arrival time to string
            item['arrival_time'] = convert_time_to_string(item['arrival_time'])

            # also add the information of related eatery
            item["eatery_name"] = eatery.eatery_name
            item["eatery_phone"] = eatery.phone

            # the voucher must not be expired in this list
            # this is a temporary solution, propery way should be having a expired attribute in voucher
            item['expired'] = True
            voucher_list.append(item)
    return {"vouchers": voucher_list}

# if time is not a string, conver it to a string
# if time is a string, return t
def convert_time_to_string(t):
    # if time is none, return empty string (for the arrival time)
    if not t:
        return ""
    return str(t)[:-3] if not isinstance(t, str) else t

# if date is not a string, conver it to a string
# if date is a string, return date
def convert_date_to_string(d):
    return str(d) if not isinstance(d, str) else d

# string type: "2014-06-08"     
def convert_string_to_date(s):
    # if string is empty "", return None
    if not s:
        return None
    if isinstance(s, str):
        y, m, d = s.split('-')[0], s.split('-')[1], s.split('-')[2]
        return date(int(y), int(m), int(d))
    return s

# string time type: "21:15"
def convert_string_to_time(s):
    # if string is empty "", return None
    if not s:
        return None
    if isinstance(s, str):
        h, m = s.split(':')[0], s.split(':')[1]
        return time(int(h), int(m))
    return s


# function for diner to add reviews and rating for a voucher of an eatery
# by given eatery_id, need comment and rating
# update to voucher_id, diner add review to this specific voucher
def add_review(token, voucher_id, comment, rating):
    diner = Diner.query.filter_by(token=token).first()
    # check if diner exist
    if diner is None:
        raise InputError("Invalid token")
    # check if the voucher is booked and used by the diner
    used_voucher = Voucher.query.filter_by(id=voucher_id, diner_id=diner.id, if_booked=True, if_used=True).first()
    if used_voucher is None:
        raise InputError("Invalid voucher_id")
    # check if rating is null
    if rating is None:
        raise InputError("Rating cannot be empty")

    """
    # check if the diner has already add a review to this voucher
    added_review = Review.query.filter_by(diner_id=diner.id, voucher_id=voucher_id).first()
    if added_review:
        raise InputError("Diner has already rated this voucher")
    """

    # add the review of diner into the database
    review_id = create_review(diner.id, voucher_id, comment, rating)
    
    return {'diner_id': diner.id, 'review_id': review_id}

# function for diner to edit review and rating of an eatery
def edit_review(token, review_id, rating, comment):
    diner = Diner.query.filter_by(token=token).first()
    # check if diner exist
    if diner is None:
        raise InputError("Invalid token")
    
    review = Review.query.filter_by(id=review_id, diner_id=diner.id).first()
    # check if review exist
    if review is None:
        raise InputError("Review not exist")
    
    # check if rating is null
    if not rating:
        raise InputError("Rating cannot be empty")

    review.rating = rating
    review.comment = comment
    db.session.commit()

    return {'diner_id': diner.id}

# function for diner to delete a review for an eatery.
def delete_review(token, review_id):
    diner = Diner.query.filter_by(token=token).first()
    # check if diner exist
    if diner is None:
        raise InputError("Invalid token")
    
    review = Review.query.filter_by(id=review_id, diner_id=diner.id).first()
    # check if review exist
    if review is None:
        raise InputError("Review not exist")
    # else, remove this review item from database
    remove_review(review)

    
# function for diner to get and read 
# reviews with the toatl number and average rating of an eatery from the other diners
# it works for both eatery and diner
def read_reviews(eatery_id):
    #reviews = db.session.query(Review, Diner).join(Diner, Review.diner_id==Diner.id).filter(Review.eatery_id==eatery_id).all()
    reviews = db.session.query(Voucher, Review, Diner).filter(Voucher.eatery_id==eatery_id, Voucher.diner_id==Diner.id).filter(Review.voucher_id==Voucher.id, Review.diner_id==Diner.id).all()
    #num_of_review = 0
    #sum_of_rating = 0
    if reviews is None:
        return {"reviews": []}

    review_with_diner_list = []
    for voucher, review, diner in reviews:
        item = dict((col, getattr(review, col)) for col in review.__table__.columns.keys())
        item["diner_id"] = diner.id
        item["diner_name"] = diner.first_name + " " + diner.last_name
        #num_of_review += 1
        #sum_of_rating += review.rating
        review_with_diner_list.append(item)
    
    #avg_rating = round(sum_of_rating/num_of_review, 1)
    num_of_review, avg_rating = avg_review(eatery_id)
    return {"reviews": review_with_diner_list, "review_number": num_of_review, "avg_rating": avg_rating}



# check if an eatery has already been booked by a diner before
# fixed the booked_voucher problem
def previously_booked(eatery_id, diner_id):
    booked_voucher = Voucher.query.filter_by(eatery_id=eatery_id, diner_id=diner_id, if_booked=True).first()
    if booked_voucher:
        return True
    return False

# get the avg rating by given an eatery_id
def avg_review(eatery_id):
    # get the sum of review and avg ratings of the eatery
    num_of_review = 0
    sum_of_rating = 0

    # get all used vouchers of this eatery
    reviews = db.session.query(Voucher, Review).filter(Voucher.eatery_id==eatery_id).filter(Review.voucher_id==Voucher.id).all()
    # get a list of reviews from this eatery use its voucher ids
    for voucher, review in reviews:
        num_of_review += 1
        sum_of_rating += review.rating
    # if no review, then avg rating = 0, else, avg rating is normal
    if num_of_review > 0:
        avg_rating = round(sum_of_rating/num_of_review, 1)
    else:
        avg_rating = 0
    return num_of_review, avg_rating

# function for getting recommendations based on diner's preferences
# for an eatery to see all eateries that I have not rpeviously had a booking
# I may be interested in -> high avg rating
# from preiviously booked voucher to see diner's preferenece
# given diner's token
def get_recommendations(token):
    diner = Diner.query.filter_by(token=token).first()
    # check if diner exist
    if diner is None:
        raise InputError("Invalid token")
    # eatery that has not been previously booked by the diner,
    # and may with a avg rating > 3
    eateries = Eatery.query.all()
    recomm_eateries = []
    diner_id = diner.id
    # get all eateries from database
    for eatery in eateries:
        # if a eatery has already previously booked by the diner, skip
        # at the same time, the eatery has high avg rating
        if avg_review(eatery.id)[1] > 3:
            # get all the info of eatery
            eatery_item = dictionary_of_eatery(eatery)
            # get the first image of the eatery
            first_image = Image.query.filter_by(eatery_id=eatery.id).first()
            eatery_item["eatery_image"] = first_image.image if first_image else ''

            num_of_review, avg_rating = avg_review(eatery.id)

            eatery_item["num_of_review"] = num_of_review
            eatery_item["avg_rating"] = avg_rating

            # add the eatery with image dictionary into the list
            recomm_eateries.append(eatery_item)

    return recomm_eateries

# function for sorting the review by the rating, positive or negative.
# top down or down top, negative or positive
def sort_reviews(sort_by, eatery_id):
    # if the user want to see top down review(positive first)
    if sort_by == "positive_first":
        reviews = db.session.query(Review, Diner).join(Diner, Review.diner_id==Diner.id).filter(Review.eatery_id==eatery_id).order_by(Review.rating).all()
    else:
        reviews = db.session.query(Review, Diner).join(Diner, Review.diner_id==Diner.id).filter(Review.eatery_id==eatery_id).order_by(Review.rating.desc()).all()
    if reviews is None:
        return {"reviews": "There is no review yet"}

    review_with_diner_list = []
    for review, diner in reviews:
        item = dict((col, getattr(review, col)) for col in review.__table__.columns.keys())
        item["diner_id"] = diner.id
        item["diner_name"] = diner.first_name + " " + diner.last_name
        
        #num_of_review += 1
        #sum_of_rating += review.rating
        review_with_diner_list.append(item)
    
    #avg_rating = round(sum_of_rating/num_of_review, 1)
    num_of_review, avg_rating = avg_review(eatery_id)
    return {"reviews": review_with_diner_list, "review_number": num_of_review, "avg_rating": avg_rating}

# function for sorting the eatery by their avg_rating
# User can choose positive first(highest rate) or negative first()
# eatery_list is a list of dictionary of eatery
"""
[{
    "id": xxx,
    "first_name": xxx,
    ...
    "eatert_name": xxx,
    "address": xxx,
    "image": xxx,
    "sum_of_review": xxx,
    "avg_rating": xxx
}, {}]
"""
def sort_eateries(sort_by, eatery_list):
    # if user didn't select sort_by, do nothing
    if sort_by is None:
        return eatery_list
    elif sort_by == "positive_first":
        sorted_eatery = sorted(eatery_list, key=lambda eatery: eatery["avg_rating"])
        return sorted_eatery
    else:  # sort_by == "negative_first":
        sorted_eatery = sorted(eatery_list, key=lambda eatery: eatery["avg_rating"], reverse=True)
        return sorted_eatery