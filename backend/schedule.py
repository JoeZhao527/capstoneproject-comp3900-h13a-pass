
def add_schedule(token, weekday, start, end, discount, voucher_num, eatery_id):
    '''
    Checks discount 
    Checks if a valid eatery_id
    Checks if token is valid (decode)?
    '''
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    
    schedule = Schedule(token, weekday, voucher_num, discount, start, end, eatery_id)
    db.session.add(schedule)
    db.session.commit()
    return schedule

def update_schedule(token, weekday, start, end, discount, voucher_num, eatery_id, schedule_id):
    '''
    Checks discount
    Checks if token is valid
    Checks if schedule and eatery id is valid
    '''
    if discount > 100:
        raise InputError("Discount cannot be greater than 100")
    
    schedule = Schedule.query.filter_by(eatery_id=eatery_id, weekday=weekday)
    schedule.voucher_num = voucher_num
    schedule.discount = discount
    schedule.start = start
    schedule.end = end
    db.session.commit()


def remove_schedule(token, weekday, schedule_id, eatery_id):
    db.session.query(Schedule).filter_by(eatery_id=eatery_id, weekday=weekday).delete()
    db.session.commit()