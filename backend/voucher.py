from server import db
from .user_db import *
from exceptions.errors import *
from datetime import date, datetime, time

def add_voucher(token, voucher_date, start, end, discount, eatery_id):
    # Check if discount exceeds 100
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    # Checks if it is a valid time-range
    if end <= start:
        raise InputError("Invalid time range")
    # Check if present time is already passed the given date and time range.
    if voucher_date < date.today():
        raise InputError("Already past the vouchers date")
    if not start <= datetime.now().time() <= end:
        raise InputError("Current time is not in vouchers time-range")

    voucher = Voucher(eatery_id, date, start, end, discount)
    voucher_id = voucher.id
    db.session.add(voucher)
    db.session.commit()
    # GENERATE CODE
    code = ""
    
    return { voucher_id, code }

def update_voucher(token, voucher_id, voucher_date, start, end, discount, if_used):
    # Check if discount exceeds 100
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    # Checks if it is a valid time-range
    if end <= start:
        raise InputError("Invalid time range")
    # Check if present time is already passed the given date and time range.
    if voucher_date < date.today():
        raise InputError("Already past the vouchers date")
    if not start <= datetime.now().time() <= end:
        raise InputError("Current time is not in vouchers time-range")

    voucher = db.session.query(Voucher).filter_by(id=voucher_id)
    voucher.date = voucher_id
    voucher.start_time = start
    voucher.end_time = end
    voucher.discount = discount
    db.session.commit()

    return {}

def remove_voucher(token, voucher_id):
    if not db.session.query(Voucher).filter_by(id=voucher_id).scalar():
        raise InputError("Invalid voucher id")

    db.session.query(Voucher).filter_by(id=voucher_id).delete()
    db.session.commit()

    return {}