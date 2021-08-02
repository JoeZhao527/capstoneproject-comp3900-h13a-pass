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

def test_eatery_register_invalid_email2():
    clear_db()
    email = ""
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

def test_eatery_register_invalid_password2():
    clear_db()
    email = "hi@qq.com"
    password = ""
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


def test_eatery_register_invalid_password3():
    clear_db()
    email = "hi@qq.com"
    password = "11111"
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

def test_eatery_register_invalid_address2():
    clear_db()
    email = "hi@qq.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "joe's dinning"
    address = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
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
def test_eatery_register_invalid_name():
    clear_db()
    email = "11111111@gmail.com"
    password = "12345678"
    first_name = ""
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

def test_eatery_register_invalid_name2():
    clear_db()
    email = "11111111@gmail.com"
    password = "12345678"
    first_name = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
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

def test_eatery_register_invalid__eatery_name():
    clear_db()
    email = "11111111@gmail.com"
    password = "12345678"
    first_name = ""
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    address = "21-2 My Street"
    menu = ''
    cuisine = ''
    city = "Syndey"
    suburb = "Kensington"
    description = ''
    with pytest.raises(InputError):
        eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
            menu, cuisine, city, suburb, description)

def test_eatery_register_invalid_address():
    clear_db()
    email = "11111111@gmail.com"
    password = "12345678"
    first_name = ""
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "joe's dinning"
    address = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    menu = ''
    cuisine = ''
    city = "Syndey"
    suburb = "Kensington"
    description = ''
    with pytest.raises(InputError):
        eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
            menu, cuisine, city, suburb, description)


def test_eatery_register_invalid_menu():
    clear_db()
    email = "11111111@gmail.com"
    password = "12345678"
    first_name = ""
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "joe's dinning"
    address = "21-2 My Street"
    menu = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    cuisine = ''
    city = "Syndey"
    suburb = "Kensington"
    description = ''
    with pytest.raises(InputError):
        eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
            menu, cuisine, city, suburb, description)


def test_eatery_register_invalid_city():
    clear_db()
    email = "11111111@gmail.com"
    password = "12345678"
    first_name = ""
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "joe's dinning"
    address = "21-2 My Street"
    menu = ''
    cuisine = ''
    city = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    suburb = "Kensington"
    description = ''
    with pytest.raises(InputError):
        eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
            menu, cuisine, city, suburb, description)

def test_eatery_register_invalid_suburb():
    clear_db()
    email = "11111111@gmail.com"
    password = "12345678"
    first_name = ""
    last_name = "zhao"
    phone = "061726371"
    eatery_name = "joe's dinning"
    address = "21-2 My Street"
    menu = ''
    cuisine = ''
    city = 'city'
    suburb = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    description = ''
    with pytest.raises(InputError):
        eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
            menu, cuisine, city, suburb, description)


def test_diner_register_success():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    res = diner_register(email, password, first_name, last_name, phone)
    assert res['diner_id'] == 1 and len(res['token']) == 105

def test_diner_register_invalid_email():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    with pytest.raises(InputError):
        diner_register(email, password, first_name, last_name, phone)

def test_diner_register_used_email():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    diner_register(email, password, first_name, last_name, phone)
    with pytest.raises(InputError):
        diner_register(email, password, first_name, last_name, phone)
    
def test_diner_register_invalid_name():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = ""
    last_name = "zhao"
    phone = "061726371"
    with pytest.raises(InputError):
        diner_register(email, password, first_name, last_name, phone)
    
def test_diner_register_invalid_name2():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    last_name = "zhao"
    phone = "061726371"
    
    with pytest.raises(InputError):
        diner_register(email, password, first_name, last_name, phone)
    
def test_diner_register_invalid_name3():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = " "
    last_name = ""
    phone = "061726371"
    with pytest.raises(InputError):
        diner_register(email, password, first_name, last_name, phone)
    
def test_diner_register_invalid_name():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = ""
    last_name = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    phone = "061726371"
    # diner_register(email, password, first_name, last_name, phone)
    with pytest.raises(InputError):
        diner_register(email, password, first_name, last_name, phone)
    

def test_eatery_login_success():
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
    eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
        menu, cuisine, city, suburb, description)
    res = eatery_login(email, password)
    assert res['eatery_id'] == 1 and len(res['token']) == 99

def test_eatery_login_fail():
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
    # eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
    #     menu, cuisine, city, suburb, description)
    with pytest.raises(InputError):
        res = eatery_login(email, password)
    # assert res['eatery_id'] == 1 and len(res['token']) == 99

def test_diner_login_success():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    diner_register(email, password, first_name, last_name, phone)
    # with pytest.raises(InputError):
    res = diner_login(email, password)
    assert res['diner_id'] == 1 and len(res['token']) == 99



def test_diner_login_fail():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    # diner_register(email, password, first_name, last_name, phone)
    with pytest.raises(InputError):
        res = diner_login(email, password)
    # assert res['diner_id'] == 1 and len(res['token']) == 99

def test_auth_logout_success():
    clear_db()
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    res = diner_register(email, password, first_name, last_name, phone)
    token = res['token']
    res = auth_logout(token)
    assert res["logout_success"]==True

# def test_diner_password_request_test():
#     clear_db()
#     email = "12345678@gmail.com"
#     password = "12345678"
#     first_name = "joe"
#     last_name = "zhao"
#     phone = "061726371"
#     res = diner_register(email, password, first_name, last_name, phone)
    
#     assert diner_password_request(email) =={}

# def test_aut_password_request_test():
#     clear_db()
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
#     eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
#         menu, cuisine, city, suburb, description)
    
#     assert auth_password_request(email) =={}


def test_diner_update_success():
    # clear up database
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    
    # eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
    #     menu, cuisine, city, suburb, description)
    diner_register(email, password, first_name, last_name, phone)
    res = diner_login(email, password)
    token = res["token"]
    # with pytest.raises(InputError):
    # res = diner_login(email, password)
    first_name = "oje"
    res = diner_profile_update(token, first_name, last_name, phone)
    assert res['first_name'] == "oje"

def test_eatery_update_fail():
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
    eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
         menu, cuisine, city, suburb, description)
    # diner_register(email, password, first_name, last_name, phone)
    res = eatery_login(email, password)
    token = res["token"]
    # with pytest.raises(InputError):
    # res = diner_login(email, password)
    first_name = "oje"
    with pytest.raises(InputError):
        
        # res = eatery_profile_update('1', first_name, last_name, phone, eatery_name, address, menu, cuisine, city, suburb, description)
    
        res = eatery_profile_update('1', first_name, last_name, phone, eatery_name, address, menu, cuisine, city, suburb, description)
    # assert res['first_name'] == "oje"
def test_eatery_update_success():
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
    eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
         menu, cuisine, city, suburb, description)
    # diner_register(email, password, first_name, last_name, phone)
    res = eatery_login(email, password)
    token = res["token"]
    # with pytest.raises(InputError):
    # res = diner_login(email, password)
    first_name = "oje"
    res = eatery_profile_update(token, first_name, last_name, phone, eatery_name, address, menu, cuisine, city, suburb, description)
    assert res['first_name'] == "oje"
def test_eatery_update_fail():
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
    eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
         menu, cuisine, city, suburb, description)
    # diner_register(email, password, first_name, last_name, phone)
    res = eatery_login(email, password)
    token = res["token"]
    # with pytest.raises(InputError):
    # res = diner_login(email, password)
    first_name = "oje"
    with pytest.raises(InputError):
        
        res = eatery_profile_update('1', first_name, last_name, phone, eatery_name, address, menu, cuisine, city, suburb, description)
    # assert res['first_name'] == "oje"

def test_diner_profile_update():
    clear_db()
    # sign up a eatery use backend functions
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    
    # eatery_register(email, password, first_name, last_name, phone, eatery_name, address, 
    #     menu, cuisine, city, suburb, description)
    diner_register(email, password, first_name, last_name, phone)
    res = diner_login(email, password)
    token = res["token"]
    # with pytest.raises(InputError):
    # res = diner_login(email, password)
    first_name = "o"
    res = diner_profile_update(token, first_name, last_name, phone)
    assert res['first_name']=='o'

def test_diner_valid_token():
    assert diner_valid_token("1")==False

def test_eatery_valid_token():
    assert eatery_valid_token("1")==False