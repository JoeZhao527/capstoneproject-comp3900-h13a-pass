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

##################################################
##           eatery_register test               ##
##################################################

# test for successfully register an eatery
def test_eatery_register_success():
    # clear up database
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
    assert res['eatery_id'] == 1 and len(res['token']) == 105

# test for trying to register with invalid email
def test_eatery_register_invalid_email():
    clear_db()
    email = "trash email"
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
    with pytest.raises(InputError):
        eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
            menu, cuisine, city, suburb, description)

# test for trying to register with repeated email
def test_eatery_register_repeated_email():
    clear_db()
    email = "11111111@gmail.com"
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
    eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
        menu, cuisine, city, suburb, description)
    with pytest.raises(InputError):
        eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
            menu, cuisine, city, suburb, description)


##################################################
##            diner_register test               ##
##################################################

# TODO: ADD MORE TESTS
