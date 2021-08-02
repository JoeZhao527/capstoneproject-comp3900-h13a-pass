# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.auth import *
from backend.user_db import *

from datetime import date, datetime, time, timedelta
from server import db
import string
import random

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# function for cheking valid eatery
def valid_eatery(eatery_id, token):
    eatery = Eatery.query.filter_by(id=eatery_id, token=token).first()
    # no eatery with given id or given token in the data
    if eatery is None:
        return False
    return True

# function for creating an voucher item and add into the voucher table
def create_voucher(eatery_id, date, start_time, end_time, discount, code, group_id):
    new_voucher = Voucher(eatery_id, date, start_time, end_time, discount, code, group_id)
    add_item(new_voucher)
    return new_voucher


# function for adding item in the database
def add_item(item):
    db.session.add(item)
    db.session.commit()

# function for deleting item in the database
def delete_item(item):
    db.session.delete(item)
    db.session.commit()

# function for generating voucher
def add_voucher(token, eatery_id, date, start, end, discount):
    start, end = convert_string_to_time(start), convert_string_to_time(end)
    date = convert_string_to_date(date)
    # check if eatery is valid by check the eatery id and token
    if not valid_eatery(eatery_id, token):
        raise InputError("Invalid token")
    # check if the voucher date and time is valid
    if date < date.today() or (date == date.today() and end < datetime.now().time()):
        raise InputError("Voucher Time invalid")
    # check if the voucher ends before it starts
    if end <= start:
        raise InputError("Invalid Voucher range")

    # creating a radom verify code for eatery and user to cehck the voucher
    mix = string.ascii_letters + string.digits
    code = ''.join(random.choice(mix) for i in range(20))

    # check if the voucher already had a group
    voucher_group_id = db.session.query(Voucher.group_id).filter(Voucher.eatery_id == eatery_id, Voucher.date == date, Voucher.start_time == start, Voucher.end_time == end, Voucher.discount == discount).first()
    # if voucher does not belong to any of the group, generate a new group id
    if voucher_group_id is None:
        num_vouchers = len(Voucher.query.all())
        group_id = 1000 + num_vouchers
    # if voucher belongs to one of the group, add the group id
    else:
        group_id = voucher_group_id[0]
    # eatery and the other info are valid
    # create the voucher (convert the date into weekday)
    voucher = create_voucher(eatery_id, date, start, end, discount, code, group_id)
    voucher.if_used = False
    voucher.if_booked = False
    voucher.weekday = weekdays[date.weekday()] # datetime.datime.today().weekday()
    db.session.commit()

    return {"voucher_id": voucher.id, "group_id": group_id}

# function for generating voucher without token
def add_voucher_by_schedule(eatery_id, date, start, end, discount, schedule_id):
    start, end = convert_string_to_time(start), convert_string_to_time(end)
    date = convert_string_to_date(date)
    # check if the voucher date and time is valid
    if date < date.today() or (date == date.today() and end < datetime.now().time()):
        raise InputError("Voucher Time invalid")
    # check if the voucher ends before it starts
    if end <= start:
        raise InputError("Invalid Voucher range")

    # creating a radom verify code for eatery and user to cehck the voucher
    mix = string.ascii_letters + string.digits
    code = ''.join(random.choice(mix) for i in range(20))

    # check if the voucher already had a group
    voucher_group_id = db.session.query(Voucher.group_id).filter(Voucher.eatery_id == eatery_id, Voucher.date == date, Voucher.start_time == start, Voucher.end_time == end, Voucher.discount == discount).first()
    # if voucher does not belong to any of the group, generate a new group id
    if voucher_group_id is None:
        num_vouchers = len(Voucher.query.all())
        group_id = 1000 + num_vouchers
    # if voucher belongs to one of the group, add the group id
    else:
        group_id = voucher_group_id[0]
    # eatery and the other info are valid
    # create the voucher (convert the date into weekday)
    voucher = create_voucher(eatery_id, date, start, end, discount, code, group_id)
    voucher.if_used = False
    voucher.if_booked = False
    voucher.weekday = weekdays[date.weekday()] # datetime.datime.today().weekday()
    voucher.schedule_id = schedule_id
    db.session.commit()

    return {"voucher_id": voucher.id, "group_id": group_id}



# function for updating the voucher, date-> weekday, start time, end time, discount etc.
# not rlly got used, but if need to use, remember to update group id
def update_voucher(token, voucher_id, date, start, end, discount):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the token by the vouchr_id(eatery_id just in case)
    voucher = Voucher.query.filter_by(id=voucher_id, eatery_id=eatery.id).first()

    voucher.date = date
    voucher.start = start
    voucher.end = end
    voucher.discount = discount
    voucher.weekday = date.weekday() # datetime.datime.today().weekday()
    db.session.commit()

# function for deleting the voucher
def delete_all_vouchers(token, group_id):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the voucher and delete it 
    vouchers = Voucher.query.filter_by(group_id=group_id, eatery_id=eatery.id, if_booked=False).all()
    for voucher in vouchers:
        delete_item(voucher)

# function for deleting the voucher by group_id
def delete_voucher_by_group(token, group_id):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the first voucher in the group and delete it
    voucher = Voucher.query.filter_by(group_id=group_id, eatery_id=eatery.id).first()
    delete_item(voucher)

def delete_voucher_by_id(token, voucher_id):
    try:
        eatery = Eatery.query.filter_by(token=token).first()
        if eatery is None:
            raise InputError("invalid token")

        voucher = Voucher.query.filter_by(id=voucher_id, eatery_id=eatery.id).first()
        delete_item(voucher)
    except:
        pass

# function for checking if a voucher has expired or not
# by given a voucher item, check if this voucher has expired
def voucher_has_expired(voucher):
    # if voucher is used, then it is not expired
    if voucher.if_used:
        return False
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


# get all eatery's unbooked vouchers by eatery's token
# 1. not booked and not expired
def get_unbooked_voucher(token):
    if type(token) == str:
        eatery = Eatery.query.filter_by(token=token).first()
    else:
        eatery = Eatery.query.filter_by(id=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []
    '''
    each voucher in voucher list have the following structure:
        {
            amount: 3       - this is for frontend showing voucher purpose, not in database
            code: "qaCam8etuN0pyxb8ZzUe"
            date: "2021-07-17"
            diner_id: null
            discount: 10
            eatery_id: 1
            end_time: "23:49"
            group_id: 1000
            id: 1
            if_booked: false
            if_used: false
            start_time: "21:49"
            weekday: "Saturday"
        }
    '''
    # get all the voucher query
    # store the unbooked vouchers into list
    # for the voucher has not booked
    for voucher in Voucher.query.filter_by(eatery_id=eatery.id, if_booked=False).all():
        # and the voucher has not expired        
        if not voucher_has_expired(voucher):
            item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
            # convert the start and end time to string
            item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
            item['date'] = convert_date_to_string(item['date'])
            
            # conver the arrival time to string
            # item['arrival_time'] = convert_time_to_string(item['arrival_time'])
            
            # add an extra attribute
            # amount of this type of voucher
            item['amount'] = 1

            # append voucher_group to voucher list
            voucher_group_append(voucher_list, item)

    return {"vouchers": voucher_list}

# group voucher and append to voucher list
def voucher_group_append(voucher_list, voucher):
    # group the voucher by their group id
    for item in voucher_list:
        if item['group_id'] == voucher['group_id']:
            item['amount'] += 1                 
            return  # jump out of the function
    # else append the item seperately into the voucher_list 
    voucher_list.append(voucher)

# get all eatery's unbooked and expired vouchers by eatery's token
# 2. not booked and expired --> can also group them
def get_unbooked_expired_voucher(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are not booked and also expired
    for voucher in Voucher.query.filter(eatery_id=eatery.id, if_booked=False).all():
        # and the voucher has expired        
        if voucher_has_expired(voucher):
            item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
            # convert the start and end time to string
            item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
            item['date'] = convert_date_to_string(item['date'])
            
            # conver the arrival time to string
            # item['arrival_time'] = convert_time_to_string(item['arrival_time'])
            
            # add an extra attribute
            # amount of this type of voucher
            item['amount'] = 1

            # append voucher_group to voucher list
            voucher_group_append(voucher_list, item)
    
    return {"vouchers": voucher_list}


# get all eatery's booked, not used and not expired vouchers by eatery's token
# 3. booked, not used and not expired
# add info of review
def get_booked_diner_voucher(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are booked, not used and not expired
    voucher_diner_list = db.session.query(Voucher, Diner).join(Diner, Voucher.diner_id==Diner.id).filter(Voucher.eatery_id==eatery.id, Voucher.if_booked==True, Voucher.if_used==False).all()
    for voucher, diner in voucher_diner_list:
        # and the voucher has not expired        
        if not voucher_has_expired(voucher):
            item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
            # convert the start and end time to string
            item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
            item['date'] = convert_date_to_string(item['date'])
            
            # convert the arrival time to string
            item['arrival_time'] = convert_time_to_string(item['arrival_time'])
        
            # also add the information of related diner
            item["diner_name"] = diner.first_name + " " + diner.last_name
            item["diner_phone"] = diner.phone

            # the voucher must not be expired in this list
            # this is a temporary solution, propery way should be having a expired attribute in voucher
            item['expired'] = False
            voucher_list.append(item)
    return {"vouchers": voucher_list}


# get all eatery's booked, not used but expired vouchers by eatery's token
# 4. booked, not used but expired
# also include the info of diner
def get_booked_expired_voucher(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are booked, not used but expired
    voucher_diner_list = db.session.query(Voucher, Diner).join(Diner, Voucher.diner_id==Diner.id).filter(Voucher.eatery_id==eatery.id, Voucher.if_booked==True).all()
    for voucher, diner in voucher_diner_list:
        # and the voucher has expired   
        if voucher_has_expired(voucher):
            item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
            # convert the start and end time to string
            item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
            item['date'] = convert_date_to_string(item['date'])
            
            # conver the arrival time to string
            item['arrival_time'] = convert_time_to_string(item['arrival_time'])
            
            # also add the information of related diner
            item["diner_name"] = diner.first_name + " " + diner.last_name
            item["diner_phone"] = diner.phone

            # the voucher must be expired in this list
            # this is a temporary solution, propery way should be having a expired attribute in voucher
            item['expired'] = True
            voucher_list.append(item)
    return {"vouchers": voucher_list}

# 5. vouchers booked and used
# (add comment(s) and rating(s) from the diner if the diner has add reviews)
def get_booked_used_voucher(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are booked and used
    voucher_diner_list = db.session.query(Voucher, Diner).join(Diner, Voucher.diner_id==Diner.id).filter(Voucher.eatery_id==eatery.id, Voucher.if_booked==True, Voucher.if_used==True).all()
    for voucher, diner in voucher_diner_list:
        item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
        # convert the start and end time to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        item['date'] = convert_date_to_string(item['date'])
        
        # conver the arrival time to string
        item['arrival_time'] = convert_time_to_string(item['arrival_time'])
        
        # also add the information of related diner
        item["diner_name"] = diner.first_name + " " + diner.last_name
        item["diner_phone"] = diner.phone

        # booked and voucher can be expired or not expired
        item['expired'] = True if voucher_has_expired(voucher) else False
        
        # added reviews by the diner who use the voucher to each voucher item in the voucher list (rating with comments)
        item['reviews'] = []
        reviews = Review.query.filter_by(voucher_id=voucher.id, diner_id=diner.id).all()
        # if diner has add some reviews
        # add them one by one into the voucher_item['reviews'] list
        if reviews:
            for review in reviews:
                item['reviews'].append({"rating": review.rating, "comment": review.comment})
        # else the reviews list is a empty list
        voucher_list.append(item)
    
    return {"vouchers": voucher_list}

# 6. all booked, (used or not used) and (both expired and not expired)
# (update)
def get_all_diner_voucher(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    voucher_list = []

    # to get all the vouchers that are booked, not used and not expired
    voucher_diner_list = db.session.query(Voucher, Diner).join(Diner, Voucher.diner_id==Diner.id).filter(Voucher.eatery_id==eatery.id, Voucher.if_booked==True).all()
    for voucher, diner in voucher_diner_list:
        item = dict((col, getattr(voucher, col)) for col in voucher.__table__.columns.keys())
        # convert the start and end time to string
        item['start_time'], item['end_time'] = convert_time_to_string(item['start_time']), convert_time_to_string(item['end_time'])
        item['date'] = convert_date_to_string(item['date'])
        
        # conver the arrival time to string
        item['arrival_time'] = convert_time_to_string(item['arrival_time'])
        
        # also add the information of related diner
        item["diner_name"] = diner.first_name + " " + diner.last_name
        item["diner_phone"] = diner.phone

        # if voucher is expired, set expired to be true
        # this is a temporary solution, propery way should be having a expired attribute in voucher
        item['expired'] = True if voucher_has_expired(voucher) else False
        
        
        # added reviews by the diner who use the voucher to each voucher item in the voucher list (rating with comments)
        item['reviews'] = []
        reviews = Review.query.filter_by(voucher_id=voucher.id, diner_id=diner.id).all()
        # if diner has add some reviews
        # add them one by one into the voucher_item['reviews'] list
        if reviews:
            for review in reviews:
                item['reviews'].append({"rating": review.rating, "comment": review.comment})
        # else the reviews list is a empty list
        
        
        voucher_list.append(item)
    return {"vouchers": voucher_list}

# use eatery token and voucher_id to complete a reservation
# when diner show the 
def complete_booking(token, voucher_id):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")
    
    # find voucher by voucher id
    voucher = Voucher.query.filter_by(id=voucher_id).first()
    if voucher is None:
        raise InputError("Invalid voucher id")

    # TODO: check if current time is in voucher‘s time range
    voucher.if_used = True
    db.session.commit()
    return

# get analytic data for eatery
def get_analytic(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # check if eatery exist
    if eatery is None:
        raise InputError("Invalid token")

    rating_num = []
    for i in range(1,6):
        review_num = len(db.session.query(Voucher, Review).join(Review, Review.voucher_id==Voucher.id).filter(Voucher.eatery_id==eatery.id, Review.rating==i).all())
        rating_num.append(review_num)
    today = date.today()
    # list of number of completed reservation for past 7 days
    complete_num = []

    for i in range(6,-1,-1):
        curr_date = today - timedelta(days=i)
        reservation_today = len(Voucher.query.filter_by(eatery_id=eatery.id, date=curr_date, if_used=True).all())
        complete_num.append(reservation_today)
    
    return { 'line': complete_num, 'doughnut': rating_num }


    pass
# string type: "2014-06-08"     
def convert_string_to_date(s):
    if isinstance(s, str):
        y, m, d = s.split('-')[0], s.split('-')[1], s.split('-')[2]
        return date(int(y), int(m), int(d))
    return s

# string time type: "21:15"
def convert_string_to_time(s):
    if isinstance(s, str):
        h, m = s.split(':')[0], s.split(':')[1]
        return time(int(h), int(m))
    return s

# if time is not a string, conver it to a string
# if time is a string, return t
def convert_time_to_string(t):
    return str(t)[:-3] if not isinstance(t, str) else t

# if date is not a string, conver it to a string
# if date is a string, return date
def convert_date_to_string(d):
    return str(d) if not isinstance(d, str) else d