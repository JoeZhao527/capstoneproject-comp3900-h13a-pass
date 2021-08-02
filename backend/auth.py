import string
import random
import jwt
import re
import hashlib
import smtplib
from email.message import EmailMessage

# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.user_db import Eatery, Diner, Voucher
from backend.data_access import create_eatery, create_diner, get_eatery_by_token, get_diner_by_token, update_eatery_token, dictionary_of_eatery, store_image, dictionary_of_voucher
from backend.errors import InputError
from server import db
# for loading data
import json

# for testing
from backend.voucher import convert_date_to_string, create_voucher, add_voucher
from datetime import date, datetime, time

# for the eatery register and create voucher (load data from json file into the database)
#from backend.voucher import create_voucher
#from backend.data_access import store_image


VALID_EMAIL = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

# function for generating a token by given uid
def generate_token(u_id):
    # generate SECRET by using radom string--> len(random String) == 20
    letters = string.ascii_letters
    secret = ''.join(random.choice(letters) for i in range(20))
    token = jwt.encode({'user_id': u_id}, secret, algorithm='HS256')
    return token

# function for hashing a password to protect the security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# function for checking if the email is used by an eatery
def eatery_email_used(email):
    eatery = Eatery.query.filter_by(email=email).first()
    # someone eatery used this email,
    if eatery is not None:
        return True
    return False

# function for checking if the email is used by an diner
def diner_email_used(email):
    diner = Diner.query.filter_by(email=email).first()
    # someone eatery used this email,
    if diner is not None:
        return True
    return False

'''
# function for adding item in the database
def add_item(item):
    db.session.add(item)
    db.session.commit()

# function for creating an eatery item and add into the eatery table
def create_eatery(first_name, last_name, email, password, phone, eatery_name, address, menu, description, token):
    eatery = Eatery(first_name, last_name, email, password, phone, eatery_name, address, menu, description, token)
    add_item(eatery)
    return eatery.id

# function for creating an diner item
def create_diner(first_name, last_name, email, password, phone, token):
    diner = Diner(first_name, last_name, email, password, phone, token)
    add_item(diner)
    return diner.id
'''


# a function that create a new account for the eatery by given valid email, password, name and phone
def eatery_register(email, password, first_name, last_name, phone, eatery_name, address, menu, cuisine, city, suburb, description):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email is invalid")
    # check if the email addess is being used by another eatery
    if eatery_email_used(email):
        raise InputError("Email being used")
    # check if the password entered is less than 6 character(or empty)
    if len(password) < 6:
        raise InputError("Password cannot be less than 6 digit")
    # check if first name or last name is empty
    if not first_name:
        raise InputError("First name is empty")
    if not last_name:
        raise InputError("Last name is empty")
    # check if first name or last name is invalid
    if len(first_name) > 50:
        raise InputError("First name is too long")
    if len(last_name) > 50:
        raise InputError("Last name is too long")

    # check if the eatery_name, address, menu, desciption is valid...
    if len(eatery_name) > 50:
        raise InputError("Eatery name is too long")
    if len(address) > 50:
        raise InputError("Eatery address is too long")
    if len(menu) > 50:
        raise InputError("Eatery menu invalid")
    if len(description) > 1000:
        raise InputError("description is too long")
    if len(city) > 20:
        raise InputError("Eatery city is too long")
    if len(suburb) > 20:
        raise InputError("Eatery suburb is too long")

    # hash the password for security
    hashed_password = hash_password(password)
    
    # generate user_id and token, uid = 500000 + num_of_users
    num_eateries = len(Eatery.query.all())
    userid = 500000 + num_eateries
    token = generate_token(userid)
    
    # create an eatery and store in the database, return the eatery_id
    eatery_id = create_eatery(first_name, last_name, email, hashed_password, phone, eatery_name, address, menu, cuisine, city, suburb, description, token)
    return {'eatery_id': eatery_id, 'token': token}

# a function that create a new account for the diner by given valid email, password, name and phone
def diner_register(email, password, first_name, last_name, phone):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email addess is being used by another diner
    if diner_email_used(email):
        raise InputError("Email being used")
    # check if the password entered is less than 6 character(or empty)
    if len(password) < 6:
        raise InputError("Password invalid")
    # check if first name or last name is empty
    if not first_name:
        raise InputError("First name is empty")
    if not last_name:
        raise InputError("Last name is empty")
    # check if first name or last name is invalid
    if len(first_name) > 50:
        raise InputError("First name invalid")
    if len(last_name) > 50:
        raise InputError("Last name invalid")

    # hash the password for security
    hashed_password = hash_password(password)
    
    # generate user_id and token, uid = 100000 + num_of_users
    num_diners = len(Diner.query.all())
    userid = 100000 + num_diners
    token = generate_token(userid)
    
    # create an eatery and store in the database, return the eatery_id
    diner_id = create_diner(first_name, last_name, email, hashed_password, phone, token)
    return {'diner_id': diner_id, 'token': token}

# login function
# given a registered eatery's email and password
# generates a valid token for the eatery to remain authenticated
def eatery_login(email, passowrd):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email is registered(used)
    if not eatery_email_used(email):
        raise InputError("Email does not belong to a user")

    # email belong to a eatery, get the eatery from database
    eatery = Eatery.query.filter_by(email=email).first()
    # check if the input password match the user's password
    # if not match
    if eatery.password != hash_password(passowrd):
        raise InputError("Password Incorrect")
    # if password match, generate new token and set the user's state to login
    else:
        token = generate_token(eatery.id)
        # update token to database
        update_eatery_token(token, eatery)
        return {'eatery_id': eatery.id, 'token': token}

# login function 
# given a registered diner's email and password
# generates a valid token for the diner to remain authenticated
def diner_login(email, passowrd):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email is registered(used)
    if not diner_email_used(email):
        raise InputError("Email does not belong to a user")

    # email belong to a diner, get the diner from database
    diner = Diner.query.filter_by(email=email).first()
    # check if the input password match the user's password
    # if not match
    if diner.password != hash_password(passowrd):
        raise InputError("Password Incorrect")
    # if password match, generate new token and set the user's state to login
    else:
        token = generate_token(diner.id)
        # update token to database
        diner.token = token
        db.session.commit()

        return {'diner_id': diner.id, 'token': token}

# given an active token, invalidates the token to log the user out
# if a vaid token is given, and the user is successfully logged out -> true, otherwise -> false
# assume there won't be a diner has the same token as an eatery
# otherwise just split this function into two functions
def auth_logout(token):
    eatery = Eatery.query.filter_by(token=token).first()
    diner = Diner.query.filter_by(token=token).first()
    # if there is a eatery with the token, token valid, invalidate the token
    if eatery:
        # user.if_logged_in = False
        # end the active token of eatery
        eatery.token = None
        db.session.commit()
        return {"logout_success": True}
    # else if there is a diner with the token, invalidate the token
    elif diner:
        # end the active token of diner
        diner.token = None
        db.session.commit()
        return {"logout_success": True}
    return {"logout_success": False}

# given an email address of a registered user, send them an email contain a specific reset code
# user trying to rest the password
def auth_password_request(email):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")

    # check if the email is not registered by diner or eatery
    eatery = Eatery.query.filter_by(email=email).first()
    diner = Diner.query.filter_by(email=email).first() 
    
    
    if eatery is None and diner is None:
        raise InputError("Email does not belong to a user")
    # eatery is not none, email belongs to an eatery
    elif eatery:
        mix = string.ascii_letters + string.digits
        code = ''.join(random.choice(mix) for i in range(20))
        eatery.reset_code = code
        db.session.commit()
    elif diner:
        mix = string.ascii_letters + string.digits
        code = ''.join(random.choice(mix) for i in range(20))
        diner.reset_code = code
        db.session.commit()

    # set up the SMTP server
    # set the email server and send the 'reset_code' to the "email"
    address = "comp3900h13apass@gmail.com"
    password = "H13APASSCOMP3900"

    # set up the SMTP server
    setup = smtplib.SMTP(host='smtp.gmail.com', port=587)
    setup.starttls()
    setup.login(address, password)

    # create a message template
    msg = EmailMessage()
    msg['From'] = address
    msg['To'] = email
    msg['Subject'] = code

    setup.send_message(msg)
    setup.quit()

    return {}

def auth_password_reset(reset_code, new_password):
    # find a user with the same reset code
    eatery = Eatery.query.filter_by(reset_code=reset_code).first()
    diner = Diner.query.filter_by(reset_code=reset_code).first()
    # if reset code invalid
    if eatery is None and diner is None:
        raise InputError("Reset_code is invalid")
    # reset code valid, change the password of eatery
    elif eatery:
        if len(new_password) < 6:
            raise InputError("Invalid password")
        else:
            # change the password and empty the reset code
            hashed_password = hash_password(new_password)
            eatery.password = hashed_password
            eatery.reset_code = ""
            db.session.commit()
    # reset code valid, change the password of diner
    elif diner:
        if len(new_password) < 6:
            raise InputError("Invalid password")
        else:
            # change the password and empty the reset code
            hashed_password = hash_password(new_password)
            diner.password = hashed_password
            diner.reset_code = ""
            db.session.commit()
    return {}


# function for checking if the token is valid
def eatery_valid_token(token):
    
    eatery = Eatery.query.filter_by(token=token).first()
    # diner = Diner.query.filter_by(token=token)
    if eatery is None:
        return False
    return True

def diner_valid_token(token):
    diner = Diner.query.filter_by(token=token).first()
    if diner is None:
        return False
    return True

# function for updating the eatery profile (eaterie's info), can seperate the function if necessary
def eatery_profile_update(token, first_name, last_name, phone, eatery_name, address, menu, cuisine, city, subrub, description):
    if not eatery_valid_token(token):
        raise InputError("Invalid token")
    # get eatery by token, update the info
    eatery = Eatery.query.filter_by(token=token).first()
    eatery.first_name = first_name
    eatery.last_name = last_name
    eatery.phone = phone
    eatery.eatery_name = eatery_name
    eatery.address = address
    eatery.city = city
    eatery.suburb = subrub
    eatery.cuisine = cuisine
    eatery.description = description
    if menu:
        eatery.menu = menu
    db.session.commit()
    return get_eatery_by_token(token)

# function for updating the diner profile (eaterie's info), can seperate the function if necessary
def diner_profile_update(token, first_name, last_name, phone):
    if not diner_valid_token(token):
        raise InputError("Invalid token")
    # get eatery by token, update the info
    diner = Diner.query.filter_by(token=token).first()

    diner.first_name = first_name
    diner.last_name = last_name
    diner.phone = phone
    db.session.commit()

    return get_diner_by_token(token)


# take all the information of eateries and voucher in eatery_data.json into the valueEats.db
def load_data():
    with open('../data/eatery_data.json') as data_file:
        data = json.load(data_file)
        # load eateries from the data file into the database
        for eatery in data["eateries"]:
            email = eatery["email"]
            password = eatery["password"]
            first_name = eatery["first_name"]
            last_name = eatery["last_name"]
            phone = eatery["phone"]
            eatery_name = eatery["eatery_name"]
            address = eatery["address"]
            menu = eatery["menu"]
            cuisine = eatery["cuisine"]
            city = eatery["city"]
            suburb = eatery["suburb"]
            description = eatery["description"]
            result = eatery_register(email, password, first_name, last_name, phone, eatery_name, address, menu, cuisine, city, suburb, description)
            
            
            # for each eatery, load related images
            #for image in eatery["images"]:
               # store_image(eatery_id, image)

            # load vouchers from the data file into the database
            # get the id and token of this eatery first
            eatery_id = result["eatery_id"]
            token = result["token"]
            
            # a list of voucher dictionary info
            for voucher in eatery["vouchers"]:
                date = convert_string_to_date(voucher["date"])
                start = convert_string_to_time(voucher["start_time"])
                end = convert_string_to_time(voucher["end_time"])
                discount = voucher["discount"]
                add_voucher(token, eatery_id, date, start, end, discount)


# string type: "2014-06-08"     
def convert_string_to_date(s):
    if isinstance(s, str):
        y, m, d = s.split('-')[0], s.split('-')[1], s.split('-')[2]
        return date(int(y), int(m), int(d))
    return s

# string time type: "21:15"
def convert_string_to_time(s):
    if isinstance(s, str):
        h, m = s.split(':')[0], s.split(':')[1]
        return time(int(h), int(m))
    return s
