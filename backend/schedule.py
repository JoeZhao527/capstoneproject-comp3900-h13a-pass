from sqlalchemy import *

def add_schedule(token, weekday, start, end, discount, voucher_num, eatery_id):
    '''
    Checks discount 
    Checks if a valid eatery_id
    Checks if token is valid (decode)?
    '''
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    # exists = db.session.query(db.exists().where(Eatery.id == eatery_id).scalar()
    # if not exists:
    #   raise InputError("Eatery_id ")
    schedule_id = eatery_id + 9999
    schedule = Schedule(token, weekday, voucher_num, discount, start, end, eatery_id, schedule_id)
    db.session.add(schedule)
    db.session.commit()
    return {schedule_id}

def update_schedule(token, weekday, start, end, discount, voucher_num, eatery_id, schedule_id):
    '''
    Checks discount
    Checks if token is valid
    Checks if schedule and eatery id is valid
    '''
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    # valid_ids = db.session.query(db.session.query(Schedule).filter_by(eatery_id=eatery_id, schedule_id=schedule_id)).scalar()
    # if not valid_ids:
    #   raise InputError("No existing schedule_id for this eatery_id")
    schedule = Schedule.query.filter_by(eatery_id=eatery_id, weekday=weekday)
    schedule.voucher_num = voucher_num
    schedule.discount = discount
    schedule.start = start
    schedule.end = end
    db.session.commit()
    return {}


def remove_schedule(token, weekday, schedule_id, eatery_id):
    db.session.query(Schedule).filter_by(eatery_id=eatery_id, weekday=weekday).delete()
    db.session.commit()
    return {}