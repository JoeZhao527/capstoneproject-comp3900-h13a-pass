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

from backend.user_db import Eatery
from backend.data_access import create_eatery, get_eatery_by_token, update_eatery_token
from backend.errors import *


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
'''

# a function that create a new account for the eatery by given valid email, password, name and phone
def eatery_register(email, password, first_name, last_name, phone, eatery_name, address, menu, description):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email addess is being used by another eatery
    if eatery_email_used(email):
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

    # check the eatery_name, address, menu, desciption...
    # TODO


    # hash the password for security
    hashed_password = hash_password(password)
    
    # generate user_id and token, uid = 500000+ num_of_users
    num_eateries = len(Eatery.query.all())
    userid = 500000 + num_eateries
    token = generate_token(userid)
    
    # create an eatery and store in the database, return the eatery_id
    eatery_id = create_eatery(first_name, last_name, email, hashed_password, phone, eatery_name, address, menu, description, token)
    return {'eatery_id': eatery_id, 'token': token}

# login function
# given a registered user's email and password
# generates a valid token for the user to remain authenticated
def auth_login(email, passowrd):
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
# given an active token, invalidates the token to log the user out
# if a vaid token is given, and the user is successfully logged out -> true, otherwise -> false
def auth_logout(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # if there is a user with the token, token valid
    if eatery is not None:
        # user.if_logged_in = False
        eatery.token = None
        return {"logout_success": True}
    return {"logout_success": False}


# given an email address of a registered user, send them an email contain a specific reset code
# user trying to rest the password
def auth_password_request(email):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email is not registered
    if not eatery_email_used(email):
        raise InputError("Email does not belong to a user")
    else:
        eatery = Eatery.query.filter_by(email=email)
        mix = string.ascii_letters + string.digits
        code = ''.join(random.choice(mix) for i in range(20))
        eatery.reset_code = code
    
    # set up the SMTP server
    # set the email server and send the 'reset_code' to the "email"
    address = "comp3900h13apass@gmail.com"
    password = "H13APASS"

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
    eatery = Eatery.query.filter_by(reset_code=reset_code)
    # if reset code invalid
    if eatery is None:
        raise InputError("Reset_code is invalid")
    # reset code valid, change the password of eatery
    else:
        if len(new_password) < 6:
            raise InputError("Invalid password")
        else:
            hashed_password = hash_password(new_password)
            eatery.passowrd = hashed_password
            eatery.reset_code = ""
    return {}

def get_eatery(token):
    eatery = get_eatery_by_token(token)
    # TODO: check if eatery is got by this token, otherwise returns an empty string
    return eatery

if __name__ == "__main__":
    print(generate_token(123))