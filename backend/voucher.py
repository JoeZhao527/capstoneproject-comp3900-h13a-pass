from datetime import date, datetime

# function for cheking valid eatery
def valid_eatery(eatery_id, token):
    eatery = Eatery.query.filter_by(eatery_id=eatery_id, token=token)
    # no eatery with given id or given token in the data
    if eatery is None:
        return False
    return True

# function for creating an voucher item and add into the voucher table
def create_voucher(eatery_id, date, start_time, end_time, discount):
    new_voucher = Voucher(eatery_id, date, start_time, end_time, discount)
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
def add_voucher(token, date, start, end, discount, eatery_id):
    # check if eatery is valid by check the eatery id and token
    if not valid_eatery(eatery_id, token):
        raise InputError("Invalid token")
    # check if the voucher date and time is valid
    if date < date.today() or start < datetime.now().tine or end < datetime.now():
        raise InputError("Voucher Time invalid")
    
    # check if the discount is normal (between 0-1)
    if discount > 1:
        raise InputError("Voucher discount invalid")

    # eatery and the other info are valid
    # create the voucher (convert the date into weekday)
    voucher = create_voucher(eatery_id, date, start, end, discount)
    voucher.if_used = False
    voucher.if_booked = False
    weekday = date.weekday() # datetime.datime.today().weekday()
    voucher.weekday = weekday

    return {'voucher_id': voucher.id}

# function for updating the voucher
def update_voucher(token, voucher_id, date, start, end, discount):
 # check if token is valid
    eatery = eatery.query.filter_by(token=token)
    if eatery is None:
        raise InputError("Invalid token")
    voucher = Voucher.query.filter_by(voucher_id=voucher_id, eatery_id=eatery.id)

    voucher.date = date
    voucher.start = start
    voucher.end = end
    voucher.discount = discount
    weekday = date.weekday() # datetime.datime.today().weekday()
    voucher.weekday = weekday
    db.session.commit()



# function for deleting the voucher
def delete_voucher(token, voucher_id):
    # check if token is valid
    eatery = eatery.query.filter_by(token=token)
    if eatery is None:
        raise InputError("Invalid token")
    voucher = Voucher.query.filter_by(voucher_id=voucher_id, eatery_id=eatery.id)
    delete_item(voucher)







