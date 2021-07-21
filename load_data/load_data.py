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
# description words list

# cuisine list

# clear up database
def clear_db():
    db.drop_all()
    db.create_all()

def load_all():
    load_eatery(100)
    load_diner(10)
    load_voucher(10,10)
    load_image(10)
    pass