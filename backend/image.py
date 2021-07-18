# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

from backend.user_db import Eatery, Image
from backend.data_access import get_eatery_id, store_image, get_image, delete_item
from backend.errors import InputError
from server import db
from backend.auth import *

import base64

def upload_image(token, img):
    # check if token is valid
    if not eatery_valid_token(token):
        raise InputError("invalid token")
    
    # check if the image is actually uploaded
    if not img:
        raise InputError('invalid image file')
    
    # get_eatery_id and store_image is functions in data_access
    # stores the img into database and returns the image id
    eatery_id = get_eatery_id(token)
    img_id = store_image(eatery_id, img)
    return img_id

def get_eatery_image(token):
    # check if token is valid
    if not eatery_valid_token(token):
        raise InputError("invalid token")
    
    eatery_id = get_eatery_id(token)
    images = get_image(eatery_id)
    return images

def delete_image(token, image_id):
    # check if token is valid
    eatery = Eatery.query.filter_by(token=token).first()
    if eatery is None:
        raise InputError("Invalid token")
    # get the image and delete it 
    image = Image.query.filter_by(id=image_id, eatery_id=eatery.id).first()
    delete_item(image)

def get_image_by_id(eatery_id):
    images = get_image(eatery_id)
    return images