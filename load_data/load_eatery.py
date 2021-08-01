# crutial import for backend to run py itself
import os, sys
from re import sub
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *
from backend.auth import *
import random

from .progression_bar import printProgressBar
import time

# generate n eatery 
def load_eatery(n):
    loc = Location()
    name = Name()
    cui = Cuisine()
    en = EateryName()
    des = Description()

    printProgressBar(0, n, prefix = 'Progress:', suffix = '', length = 50)
    # add n eatery to database
    for i in range(1, n):
        time.sleep(0.1)
        fname, lname = name.get_name()
        email = str(i).zfill(8) + '@gmail.com'
        password = hash_password('12345678')
        phone = '0444123456'
        ename = en.get_eatery_name()
        address = '278 Sussex St'
        description = des.get_description()
        city, suburb = loc.get_location()
        cuisine = cui.get_cuisine()
        menu = None
        token = None
        eatery = Eatery(fname, lname, email, password, phone, ename, address, menu, cuisine, city, suburb, description, token)
        db.session.add(eatery)
        db.session.commit()

        printProgressBar(i + 1, n, prefix = 'Loading Eateries:', suffix = '', length = 50)
    return

# classes for eateries
class Location:
    def __init__(self) -> None:
        self.locations = {
            'Sydney': ['Kensington', 'Town Hall', 'Central', 'Burwood', 'North Sydney', 'Bondi Junction'],
            'Melbourne': ['East Melbourne', 'Flemington', 'North Melbourne', 'Parkville'],
            'Canberra': ['Forrest', 'Deakin', 'Red Hill', 'Hughes', 'Garran', 'Lyons'],
            'Adelaide': ['Henley Beach South', 'Henley Beach', 'Glenelg', 'Kensington', 'North Adelaide', 'Glenelg North']
        }
        self.cities = ['Sydney', 'Melbourne', 'Canberra', 'Adelaide']
    
    def get_location(self):
        i = random.randint(0,3)
        city = self.cities[i]
        j = random.randint(0, len(self.locations[city])-1)
        suburb = self.locations[city][j]
        return city, suburb

class Name:
    def __init__(self) -> None:
        self.first_names = "Oliver Charlotte Declan Aurora Theodore Violet Jasper Hazel Silas Luna Joe Jay Edward Karen Nicolas".split(' ')
        self.last_names = 'Smith Johnson Williams Brown Jones Garcia Miller Davis'.split(' ')
    
    def get_name(self):
        fname = self.first_names
        lname = self.last_names
        m, n = len(fname), len(lname)
        i, j = random.randint(0,m-1), random.randint(0,n-1)
        return fname[i], lname[j]

class Cuisine:
    def __init__(self) -> None:
        self.cuisine = ['Fine dinning', 'Fast food', 'Coffee', 'Noodle', 'Seafood', 'Pizza', 'Asian', 'Austrailian', 'Mexico', 'Greek']
    
    def get_cuisine(self):
        i = random.randint(0, len(self.cuisine)-1)
        j = random.randint(0, len(self.cuisine)-1)
        return self.cuisine[i] + ',' + self.cuisine[j]

class EateryName:
    def __init__(self) -> None:
        self.eatery_words = ' '.join('Excellent Experience Dine Fine Finest Dining Dinner Club Dine Dime On \
            The Dime Dining Reliable Restaurants Restaurant Resources Ready Restaurants Rocket No Rest \
            Restaurants Restaurant Recs Recommended Restaurant Restaurant Resale Tabletop Restaurants \
            Perfect Setting Forkfull Napkin Know How Perfect Place Dining Divas Kitchen Office Kitchen \
            Corral Bistro Builders Before The Bistro Restaurant Rebels Resourceful Restaurants Reel Food \
            Formula White Napkin Restaurants Full Service Dining Homey Hospitality Like Home Restaurant \
            Group Fine Dining Delivered Dining Room Ready Dining Room Resource Delightful Dining Dining \
            Delight Dedicated Dining Formal Performance Formal Foods Performance Dining Curated CuisineClick \
            to check domain availability. Cuisine Catered At Your Service Service First Service Supplied \
            Serious Service Food Factory Restaurant Warehouse Five Star Restaurants'.split(' ')).split()
    
    def get_eatery_name(self):
        ename = self.eatery_words
        i = random.sample(range(0, len(ename)), 2)
        return ename[i[0]] + ' ' + ename[i[1]]

class Description:
    def __init__(self) -> None:
        self.description_words = "Sweet Escape is Sydney's most loved home base for espresso and discussions. \
            We offer a delicious variety of coffee from Sweet Escape made by our professionally trained \
            baristas, from your classic coffee to our house specialty. You can complete your coffee with \
            oen of our sweet treats made by our very own baker We welcome you to sit back, unwind and \
            appreciate the lovely sights of the city while our best gourmet expert sets you up a scrumptious \
            dinner utilizing the best and freshest ingredients. The adaptable menu flaunts some imaginative \
            food, for example, salt and pepper squid on a delicate, Thai-roused plate of mixed greens; \
            harissa angle soup (with the harissa glue served in a little glass); lemon simmered chicken \
            on dark pepper gnocchi; and a most heavenly cinnamon. The eatery utilizes neighborhood create \
            for fish and venison dishes flourish.Excellent Experience Dine Fine Finest Dining Dinner Club Dine Dime On \
            The Dime Dining Reliable Restaurants Restaurant Resources Ready Restaurants Rocket No Rest \
            Restaurants Restaurant Recs Recommended Restaurant Restaurant Resale Tabletop Restaurants \
            Perfect Setting Forkfull Napkin Know How Perfect Place Dining Divas Kitchen Office Kitchen \
            Corral Bistro Builders Before The Bistro Restaurant Rebels Resourceful Restaurants Reel Food \
            Formula White Napkin Restaurants Full Service Dining Homey Hospitality Like Home Restaurant \
            Group Fine Dining Delivered Dining Room Ready Dining Room Resource Delightful Dining Dining \
            Delight Dedicated Dining Formal Performance Formal Foods Performance Dining Curated CuisineClick \
            to check domain availability. Cuisine Catered At Your Service Service First Service Supplied \
            Serious Service Food Factory Restaurant Warehouse Five Star Restaurants".split(' ')

        self.description = "We welcome you to sit back, unwind and appreciate the lovely sights of the city \
            while our best gourmet expert sets you up a scrumptious dinner utilizing the best and freshest \
            ingredients. The adaptable menu flaunts some imaginative food, for example, salt and pepper squid \
            on a delicate, Thai-roused plate of mixed greens; harissa angle soup (with the harissa glue served \
            in a little glass); lemon simmered chicken on dark pepper gnocchi; and a most heavenly cinnamon. \
            The eatery utilizes neighborhood create for fish and venison dishes flourish."
    def get_description(self):
        des = self.description
        return des