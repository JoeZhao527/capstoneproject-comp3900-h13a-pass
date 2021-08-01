# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.auth import *
from backend.schedule import *
from backend.data_access import *
from backend.voucher import *
from backend.image import *
from backend.diner import *
from load_data.load_data import clear_db
import pytest

# TODO: ADD SOME TESTS
# def test_add_schedule():
#     clear_db()
#     # sign up a eatery use backend functions
#     email = "12345678@gmail.com"
#     password = "12345678"
#     first_name = "joe"
#     last_name = "zhao"
#     phone = "061726371"
#     eatery_name = "joe's dinning"
#     address = "21-2 My Street"
#     menu = ''
#     cuisine = ''
#     city = "Syndey"
#     suburb = "Kensington"
#     description = ''
#     res = eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
#         menu, cuisine, city, suburb, description)
#     token = res['token']
#     eatery_id = 1
#     no_vouchers=1
#     weekday= 
#     start=
#     end= 
#     discount=
def create_eatery_for_test():
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "joe's dinning"
    address = "21-2 My Street"
    menu = ''
    cuisine = ''
    city = "Syndey"
    suburb = "Kensington"
    description = ''
    res = eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
        menu, cuisine, city, suburb, description)
    return res

def test_get_eatery_schedule():
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "joe's dinning"
    address = "21-2 My Street"
    menu = ''
    cuisine = ''
    city = "Syndey"
    suburb = "Kensington"
    description = ''
    res = eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
        menu, cuisine, city, suburb, description)
    assert get_eatery_schedule(res['token']) =={'schedules': []}

# def test_get_eatery_schedule2():
#     clear_db()
#     # sign up a eatery use backend functions
#     eatery = create_eatery_for_test()
#     token = eatery['token']
#     eatery_id = eatery['eatery_id']
#     _date = date.today() + timedelta(days=1) # tomorrow's date
#     start = time(10,30)    # 10:30
#     end = time(11,30)      # 11:30
#     discount = 20
#     res = add_voucher(token, eatery_id, _date, start, end, discount)
#     assert res['voucher_id'] == 1 and res['group_id'] == 1000 

