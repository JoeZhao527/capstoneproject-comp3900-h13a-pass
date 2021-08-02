# crutial import for backend to run py itself
from operator import truediv
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

# TODO: WRITE SOME TESTS

def test_invalid_token():
    assert valid_token("1") == False

def test_valid_token():
    clear_db()
    email = "12345678@gmail.com"
    password = "12345678"
    first_name = "joe"
    last_name = "zhao"
    phone = "061726371"
    res = diner_register(email, password, first_name, last_name, phone)
    token = res['token']
    assert valid_token(token)==True

def test_viewEatery_empty():
    clear_db()
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
    #      menu, cuisine, city, suburb, description)
    # print(view_eatery_list())
    # assert view_eatery_list() == [{'id': 1, 'first_name': 'joe', 'last_name': 'zhao', 'email': '12345678@gmail.com', 'password': 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'phone': '061726371', 'eatery_name': "joe's dinning", 'address': '21-2 My Street', 'city': 'Syndey', 'suburb': 'Kensington', 'menu': '', 'cuisine': '', 'description': '', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1MDAwMDB9.AVdPwKADNJfhqRTPIugkoAjJtKM7oP9d_Ektd6jf6Xc', 'reset_code': None}]
    assert view_eatery_list() == []

def test_search_by_key_empty():
    clear_db()
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
    #      menu, cuisine, city, suburb, description)
    # print(view_eatery_list())
    # assert view_eatery_list() == [{'id': 1, 'first_name': 'joe', 'last_name': 'zhao', 'email': '12345678@gmail.com', 'password': 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'phone': '061726371', 'eatery_name': "joe's dinning", 'address': '21-2 My Street', 'city': 'Syndey', 'suburb': 'Kensington', 'menu': '', 'cuisine': '', 'description': '', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1MDAwMDB9.AVdPwKADNJfhqRTPIugkoAjJtKM7oP9d_Ektd6jf6Xc', 'reset_code': None}]
    assert search_by_key("null") == []