# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *
from backend.auth import *
import random
import base64

from .progression_bar import printProgressBar
import time

image_dir = 'data/images'

def load_image(n):
    images = EateryImages()
    printProgressBar(0, n, prefix = 'Progress:', suffix = '', length = 50)
    for eid in range(0,n):
        time.sleep(0.1)
        for img in images.get_images(8):
            image = Image(eid, img)
            db.session.add(image)
            db.session.commit()
        printProgressBar(eid + 1, n, prefix = 'Loading Images:', suffix = '', length = 50)
    pass

class EateryImages:
    def __init__(self) -> None:
        self.data = self.read_images()

    def read_images(self):
        res = []
        for subdir, dirs, files in os.walk(image_dir):
            for file in files:
                img = self.read_img(os.path.join(subdir, file))
                res.append(img)
        return res

    # read one images
    def read_img(self, path):
        with open(path, "rb") as img_file:
            my_string = 'data:image/png;base64,' + base64.b64encode(img_file.read()).decode('utf-8')
        return my_string

    def get_images(self, num):
        image_list = self.data
        length = len(image_list)
        num = min(num, length)
        idx_list = random.sample(range(0,length),num)
        res = []
        for i in idx_list:
            res.append(image_list[i])
        return res


