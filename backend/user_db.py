from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///valueEats.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Eatery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20))
    eatery_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    menu = db.Column(db.String(50))
    description = db.Column(db.String(200))
    token = db.Column(db.String(50), unique=True)

    def __init__(self, first_name, last_name, email, password, phone_number, eatery_name, address, menu, description, token):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.eatery_name = eatery_name
        self.address = address
        self.menu = menu
        self.description = description
        self.token = token



class Diner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    
    def __init__(self, first_name, last_name, email, password, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

        
class Image(db.Model):
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'), primary_key=True)
    image = db.Column(db.String(50), nullable=False, primary_key=True)
    
    def __init__(self, eatery_id, image):
        self.eatery_id = eatery_id
        self.image = image

class Voucher(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'))
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    
    def __init__(self, eatery_id, date, start_time, end_time, discount):
        self.eatery_id = eatery_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.discount = discount

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'))
    no_vouchers = db.Column(db.Integer, nullable=False) 
    weekday = db.Column(db.String(10), nullable=False)   # Mon to Sun
    discount = db.Column(db.Float, nullable=False)
    
    def __init__(self, eatery_id, no_vouchers, weekday, discount):
        self.eatery_id = eatery_id
        self.no_vouchers = no_vouchers
        self.weekday = weekday
        self.discount = discount

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diner_id = db.Column(db.Integer, db.ForeignKey('diner.id'))
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'))
    comment = db.Column(db.String(20))
    rating = db.Column(db.Integer, nullable=False)
    
    def __init__(self, diner_id, eatery_id, comment, rating):
        self.diner_id = diner_id
        self.eatery_id = eatery_id
        self.comment = comment
        self.rating = rating


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    diner_id = db.Column(db.Integer, db.ForeignKey('diner.id'))
    eatery_id = db.Column(db.Integer, db.ForeignKey('eatery.id'))
    if_used = db.Column(db.Boolean)
    
    def __init__(self, diner_id, eatery_id, if_used):
       self.diner_id = diner_id
       self.eatery_if = eatery_id
       self.if_used = if_used

class Offer(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
     voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'))
     
     def __init__(self, schedule_id, voucher_id):
       self.schedule_id = schedule_id
       self.voucher_id = voucher_id
        
"""
CREATE DOMAIN Weekdays AS 
   CHECK (VALUE IN ('Mon','Tues','Wed','Thurs','Fri', 'Sat', 'Sun'));
CREATE DOMAIN Ratings AS 
   CHECK (VALUE > 0 AND VALUE < 6);
CREATE DOMAIN Discount AS 
   CHECK (VALUE > 0 AND VALUE <= 100);
"""

db.create_all()


def add_item(item):
    db.session.add(item)
    db.session.commit()

def create_eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, description, token):
    eatery = Eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, description, token)
    add_item(eatery)

