import string
import random
import jwt
import re
import hashlib

VALID_EMAIL = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

# function for generating a token by given uid
def generate_token(u_id):
    # generate SECRET by using radom string--> len(random String) == 25
    letters = string.ascii_letters
    secret = ''.join(random.choice(letters) for i in range(25))
    token = jwt.encode({'user_id': u_id}, secret, algorithm='HS256')
    return token

# function for hashing a password to protect the secuity
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# function for checking if the email is used (1)
def if_email_exist(email):
    return False

def diner_register(email, password, first_name, last_name, phone):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email addess is being used by another user
    if if_email_exist(email):
        raise InputError("Email being used")
    # check if the password entered is less than 6 character or empty
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
    
    # generate user_id and token, uid = 500000+user_number
    u_id = 500000
    token = generate_token(u_id)
    
    # create an eatery and store in the database (2) !!!!
    store_eatery(u_id, email, hashed_password, first_name, last_name, phone)

    return {'u_id': u_id, 'token': token}

# login function
# given a registered user's email and password
# generates a valid token for the user to remain authenticated
def auth_login(email, passowrd):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email is registered
    if not if_email_exist(email):
        raise InputError("Email does not belong to a user")

    # email belong to a user, get the user from database
    user = User.get_user_by_email(email)
    # check if the input password match the user's password
    # if not mach
    if user.password != hash_password(passowrd):
        raise InputError("Password Incorrect")
    # if password match, generate new token and set the user's state to login
    else:
        token = generate_token(user.u_id)
        user.if_logged_in = True
        
        return {'u_id': u_id, 'token': token}
# given an active token, invalidates the token to log the user out
# if a vaid token is given, and the user is successfully logged out -> true, otherwise -> false
def auth_logout(token):
    user = User.get_user_by_token(token)
    # if there is to user corresponding to token
    if user is not None:
        user.if_logged_in = False
        user.token = None
        return {"is_success": True}
    return {"is_success": False}


if __name__ == "__main__":
    print(generate_token(123))