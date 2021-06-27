import string
import random
import jwt
import re
import hashlib
import smtplib
from email.message import EmailMessage


VALID_EMAIL = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

database = {
    'userlist': [],
    'sessionlist': []
}

# function for generating a token by given uid
def generate_token(u_id):
    # generate SECRET by using radom string--> len(random String) == 25
    letters = string.ascii_letters
    secret = ''.join(random.choice(letters) for i in range(25))
    token = jwt.encode({'user_id': u_id}, secret, algorithm='HS256')
    return token

# function for hashing a password to protect the security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# function for checking if the email is used (1)
def if_email_exist(email):
    userlist = database['userlist']
    for user in userlist:
        if user['email'] == email:
            return True
    return False
# function for getting the user by email
def get_user_by_email(email):
    userlist = database['userlist']
    for user in userlist:
        if user['email'] == email:
            return user
    return None

# a function that create a new account for the eatery by given valid email, password, name and phone
def eatery_register(email, password, first_name, last_name, phone):
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
    
    # generate user_id and token, uid = 500000+user_number (2)
    userlist = database['userlist']
    u_id = 500000 + len(userlist)
    token = generate_token(u_id)
    
    # create an eatery and store in the database (3) !!!!
    new_user = {'u_id': u_id, 'email': email, 'password': hashed_password, 'first_name': first_name, 'last_name': last_name, 'phone': phone}
    userlist.append(new_user)

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
    user = get_user_by_email(email)
    # check if the input password match the user's password
    # if not mach
    if user['password'] != hash_password(passowrd):
        raise InputError("Password Incorrect")
    # if password match, generate new token and set the user's state to login
    else:
        token = generate_token(user['u_id'])
        # user.if_logged_in = True
        
        return {'u_id': user['u_id'], 'token': token}
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


# given an email address of a registered user, send them an email contain a specific reset code
# user trying to rest the password
def auth_password_request(email):
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email is registered
    if not if_email_exist(email):
        raise InputError("Email does not belong to a user")
    else:
        user = get_user_by_email(email)
        mix = string.ascii_letters + string.digits
        code = ''.join(random.choice(mix) for i in range(20))
        user['reset_code'] = code
    
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
    # reset_code is not a valid reset_code
    if not if_reset_code_exist(reset_code):
        raise InputError("Reset_code is invalid")
    else:
        if len(passowrd) < 6:
            raise InputError("Invalid password")
        else:
            user = User.get_user_by_reset_code(reset_code)
            hashed_password = hash_password(new_password)
            user.passowrd = hashed_password
            user.reset_code = ""
    return {}

if __name__ == "__main__":
    result1 = eatery_register("jianjunjchen@gmail.com", "393630Cjj", "Jay", "Chen", "0470397745")
    result2 = eatery_register("Mercy.D@gmail.com", "393630Cjj", "Jay", "Chen", "0470397745")
    result3 = auth_login("jianjunjchen@gmail.com", "393630Cjj")
    print(result1)
    print(result3)
    print(database)
    auth_password_request("jianjunjchen@gmail.com")
    
