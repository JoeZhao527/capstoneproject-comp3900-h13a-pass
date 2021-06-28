from .user_db import *

# add and commit an item to database
def add_item(item):
    db.session.add(item)
    db.session.commit()

# insert an eatery to database
def create_eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, description, token):
    eatery = Eatery(first_name, last_name, email, password, phone_number, eatery_name, address, menu, description, token)
    add_item(eatery)
    return eatery.id

# insert a Voucher to database
def create_Voucher(eatery_id, date, start_time, end_time, discount):
    voucher = Voucher(eatery_id, date, start_time, end_time, discount)
    add_item(voucher)
    return voucher.id

# insert a schedule to database
def create_Schedule(eatery_id, no_vouchers, weekday, start, end, discount, meal_type):
    schedule = Schedule(eatery_id, weekday, no_vouchers, discount, start, end, discount, meal_type)
    add_item(schedule)
    return schedule.id

# get eatery id by token
def get_eatery_id(token):
    eatery = Eatery.query.filter_by(token=token).first()
    return eatery.id

# get eatery information by id
def get_eatery_by_token(token):
    eatery = Eatery.query.filter_by(token=token).first()
    data = dict((col, getattr(eatery, col)) for col in eatery.__table__.columns.keys())
    return data

# update user token
def update_eatery_token(token, eatery):
    eatery.token = token
    db.session.commit()