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
from backend.data_access import create_eatery, create_diner, get_eatery_by_token, get_diner_by_token, update_eatery_token
from backend.errors import InputError
from server import db
# for testing
from backend.voucher import create_voucher
from datetime import date, datetime, time


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

    # check if the eatery_name, address, menu, desciption is valid...
    if len(eatery_name) > 50:
        raise InputError("Eatery name invalid")
    if len(address) > 50:
        raise InputError("Eatery address invalid")
    if len(menu) > 50:
        raise InputError("Eatery menu invalid")
    if len(description) > 1000:
        raise InputError("description invalid")
    if len(city) > 20:
        raise InputError("Eatery city invalid")
    if len(suburb) > 20:
        raise InputError("Eatery suburb invalid")

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
    eatery = Eatery.query.filter_by(token=token)
    diner = Diner.query.filter_by(token=token)
    # if there is a eatery with the token, token valid, invalidate the token
    if eatery.first():
        # user.if_logged_in = False
        # end the active token of eatery
        eatery.first().token = None
        db.session.commit()
        return {"logout_success": True}
    # else if there is a diner with the token, invalidate the token
    else:
        # end the active token of diner
        diner.first().token = None
        db.session.commit()
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
        eatery = Eatery.query.filter_by(email=email).first()
        mix = string.ascii_letters + string.digits
        code = ''.join(random.choice(mix) for i in range(20))
        eatery.reset_code = code
        db.session.commit()
    
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
    eatery = Eatery.query.filter_by(reset_code=reset_code).first()
    # if reset code invalid
    if eatery is None:
        raise InputError("Reset_code is invalid")
    # reset code valid, change the password of eatery
    else:
        if len(new_password) < 6:
            raise InputError("Invalid password")
        else:
            # change the password and empty the reset code
            hashed_password = hash_password(new_password)
            eatery.password = hashed_password
            eatery.reset_code = ""
            db.session.commit()
    return {}
    
# function for checking if the token is valid
def valid_token(token):
    eatery = Eatery.query.filter_by(token=token).first()
    # diner = Diner.query.filter_by(token=token)
    if eatery is None:
        return False
    return True

# function for updating the eatery profile (eaterie's info), can seperate the function if necessary
def eatery_profile_update(token, first_name, last_name, phone, eatery_name, address, menu, cuisine, city, subrub, description):
    if not valid_token(token):
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
    eatery.menu = menu
    eatery.cuisine = cuisine
    eatery.description = description
    db.session.commit()
    return get_eatery_by_token(token)

# function for updating the diner profile (eaterie's info), can seperate the function if necessary
def diner_profile_update(token, first_name, last_name, phone):
    if not valid_token(token):
        raise InputError("Invalid token")
    # get eatery by token, update the info
    diner = Diner.query.filter_by(token=token).first()
    diner.first_name = first_name
    diner.last_name = last_name
    diner.phone = phone
    db.session.commit()
    return get_diner_by_token(token)


if __name__ == "__main__":
    # make an eatery and add voucher
    r4 = eatery_register("5678@gmail.com", "3936Cjj", "JJI", "ASSA", "04703977", "mR.cHEN", "HHHHH RAOD", "", "", "", "" ,"")
    print(r4)
    
    new_voucher = create_voucher(r4["eatery_id"], datetime(2021, 7, 18), time(9, 50, 0), time(11, 50, 0), 0.3, "abcsefnm123")
    print(str(new_voucher.id) + "!!!!!!" + str(new_voucher.discount) + str(new_voucher.start_time))
    
    result1 = diner_register("jay123@gmail.com", "123Cjj", "Jay", "Chen", "0470397745")
    print(result1)

    result2 = diner_register("jay12345@gmail.com", "123Cjj", "Hayden", "Chen", "3000800")
    print(result2)
    #diners = Diner.query.filter_by(last_name="Chen").all()
    #for diner in diners:
    #    print(diner.email)

    #checks = db.session.query(Eatery, Voucher).filter(Voucher.eatery_id == Eatery.id).filter(Voucher.id == 1).all()
    # checks = db.session.query(Eatery).join(Voucher).filter(Eatery.last_name == "ASSA", Voucher.discount == 0.3, Voucher.end_time <= time(11, 50, 0)).all()
    #checks = Eatery.query.join(Voucher).filter(Eatery.last_name == "ASSA", Voucher.discount == 0.3, Voucher.end_time <= time(11, 50, 0)).all()
    checks = Diner.query.all()
    print(checks)
    for Eatery in checks:
        print(Eatery)
    #print(data)
    #result2 = diner_login("jay123@gmail.com", "123Cjj")
    #print(result2)

    #print(eatery.token)
    #print(eatery.phone)
    #print(eatery.eatery_name)