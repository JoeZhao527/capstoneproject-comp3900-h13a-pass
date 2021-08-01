# crutial import for backend to run py itself
import os, sys
from re import sub
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *
from backend.auth import *
import random

from load_data.load_eatery import load_eatery
from load_data.load_diner import load_diner
from load_data.load_voucher import load_voucher
from load_data.load_images import load_image
from load_data.load_reviews import load_reviews

# simply change these two value to set eatery and diner number in db
# vouchers, comment and reservations will be randomly generated from these values
eatery_number = 30
diner_number = 20

# clear up database
def clear_db():
    db.drop_all()
    db.create_all()

def load_all():
    load_eatery(eatery_number)
    print('')
    load_diner(diner_number)
    print('')
    load_voucher(30,diner_number)
    print('')
    load_image(eatery_number)
    print('')
    load_reviews(30)
    print('\nLoading data completed, enjoy your Value Eats trip!')
    pass