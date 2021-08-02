# crutial import for backend to run py itself
import os, sys
from re import sub
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server
from server import db

# datetime for voucher time range
import datetime
# clean up cache
db.metadata.clear()

class Eatery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    eatery_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(20))
    suburb = db.Column(db.String(20))
    menu = db.Column(db.String(50))
    cuisine = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    token = db.Column(db.String(200), unique=True)
    reset_code = db.Column(db.String(20))

    def __init__(self, first_name, last_name, email, password, phone, eatery_name, address, menu, cuisine, city, suburb, description, token):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.eatery_name = eatery_name
        self.address = address
        self.menu = menu
        self.cuisine = cuisine
        self.city = city
        self.suburb = suburb
        self.description = description
        self.token = token

class Diner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    token = db.Column(db.String(200), unique=True)
    reset_code = db.Column(db.String(20))
    
    def __init__(self, first_name, last_name, email, password, phone, token):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.token = token
        #self.reset_code = reset_code

        
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'))
    image = db.Column(db.Text, nullable=False)
    
    def __init__(self, eatery_id, image):
        self.eatery_id = eatery_id
        self.image = image

class Voucher(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'))
    diner_id = db.Column(db.Integer, db.ForeignKey('diner.id'))
    date = db.Column(db.Date, nullable=False)
    weekday = db.Column(db.Integer)    # dereived from date from 0 to 6
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    if_used = db.Column(db.Boolean)
    if_booked = db.Column(db.Boolean)  # add 
    code = db.Column(db.String(20))    # verify code to check if the user has booked the voucher and not used
    group_id = db.Column(db.Integer, nullable=False)   # group id for group the same vouchers 
    # scheuld_id to check if the voucher is add by a schedule
    schedule_id = db.Column(db.Integer)

    # extra attributes for diner's arrival info
    arrival_time = db.Column(db.Time)
    num_of_guest = db.Column(db.Integer)
    special_request = db.Column(db.String(200))  

    def __init__(self, eatery_id, date, start_time, end_time, discount, code, group_id):
        self.eatery_id = eatery_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.discount = discount
        self.code = code
        self.group_id = group_id
        # self.diner_id = None
        # self.if_used = False
        # self.if_booked = False
        # self.weekday = date -> weekday
        
        # self.arrival_time = None
        # self.num_of_guest = None
        # self.special_request = None
        # self.review_id = None

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.Integer, nullable=False)   # Mon to Sun (0 to 6)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    no_vouchers = db.Column(db.Integer, nullable=False) 
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'))
    # meal_type = db.Column(db.String(10), nullable=False) # breakfast, lunch, dinner

    def __init__(self, eatery_id, no_vouchers, weekday, start_time, end_time, discount):
        self.eatery_id = eatery_id
        self.no_vouchers = no_vouchers
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time
        self.discount = discount
        # self.meal_type = meal_type

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diner_id = db.Column(db.Integer, db.ForeignKey('diner.id'))
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'))
    comment = db.Column(db.String(20))
    rating = db.Column(db.Integer, nullable=False)
    
    def __init__(self, diner_id, voucher_id, comment, rating):
        self.diner_id = diner_id
        self.voucher_id = voucher_id
        self.comment = comment
        self.rating = rating
# if user run 'flask run' without "python3 load_data.py", create database here
db.create_all()