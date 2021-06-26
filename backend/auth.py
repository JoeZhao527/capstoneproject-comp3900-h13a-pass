import string
import random
import jwt
import re

VALID_EMAIL = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
def generate_token(u_id):
    """
    return a new token for authenticaiton in users' session
    Input:
    - uid (integer)

    Output:
    - token(string)
    """
    # generate SECRET by using radom string--> len(random String) == 22
    letters = string.ascii_letters
    secret = ''.join(random.choice(letters) for i in range(22))
    token = jwt.encode({'user_id': u_id}, secret, algorithm='HS256')
    return token

def diner_register(server, email, password, first_name, last_name, phone)
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email invalid")
    # check if the email addess is being used by another user
    if server.if_email.exist(email):
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
    
    



if __name__ == "__main__":
    print(generate_token(123))
