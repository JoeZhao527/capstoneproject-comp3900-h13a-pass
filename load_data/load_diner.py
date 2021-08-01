# crutial import for backend to run py itself
import os, sys
from re import sub
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *
from backend.auth import *
from load_data.load_eatery import Name
import random

from .progression_bar import printProgressBar
import time

def load_diner(n):
    name = Name()
    printProgressBar(0, n, prefix = 'Progress:', suffix = '', length = 50)
    for i in range(1, n):
        time.sleep(0.1)
        fname, lname = name.get_name()
        email = str(i).zfill(8) + '@qq.com'
        password = hash_password('12345678')
        phone = '0444123456'
        token = None
        diner = Diner(fname, lname, email, password, phone, token)
        db.session.add(diner)
        db.session.commit()
        printProgressBar(i + 1, n, prefix = 'Loading Diners:', suffix = '', length = 50)
    pass


