# crutial import for backend to run py itself
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *
from backend.auth import *
import random

from .progression_bar import printProgressBar
import time

def load_reviews(m):
    rev = EateryReviews()
    printProgressBar(0, m, prefix = 'Progress:', suffix = '', length = 50)
    for eid in range(m):
        for voucher in Voucher.query.filter_by(eatery_id=eid, if_booked=True, if_used=True).all():
            add_comment = random.randint(0,1)
            if add_comment == 0:
                for i in range(random.randint(2,5)):
                    rating, comment = rev.get_review()
                    diner_id = voucher.diner_id
                    voucher_id = voucher.id
                    review = Review(diner_id, voucher_id, comment, rating)
                    db.session.add(review)
                    db.session.commit()
        printProgressBar(eid + 1, m, prefix = 'Loading Reviews:', suffix = '', length = 50)
    pass

class EateryReviews:
    def __init__(self) -> None:
        self.words = "Sweet Escape is Sydney's most loved home base for espresso and discussions. \
            We offer a delicious variety of coffee from Sweet Escape made by our professionally trained \
            baristas, from your classic coffee to our house specialty. You can complete your coffee with \
            oen of our sweet treats made by our very own baker We welcome you to sit back, unwind and \
            appreciate the lovely sights of the city while our best gourmet expert sets you up a scrumptious \
            dinner utilizing the best and freshest ingredients. The adaptable menu flaunts some imaginative \
            food, for example, salt and pepper squid on a delicate, Thai-roused plate of mixed greens; \
            harissa angle soup (with the harissa glue served in a little glass); lemon simmered chicken \
            on dark pepper gnocchi; and a most heavenly cinnamon. The eatery utilizes neighborhood create \
            for fish and venison dishes flourish. Tastes great! Eating something delicious right now? Use \
            this expression to say so. I’m so glad I ordered this pizza—it tastes great! Really good! \
            Here’s something else you could say instead of delicious. Have you tried the chocolate cake? \
            It’s really good! Wow, [this food] is amazing! If something tastes better than you expected, \
            you could use the word wow to express your surprise. If you say something tastes amazing, you’re \
            saying it tastes even better than great or really good. Wow, this pasta salad is amazing! \
            Yummy This is an informal way of saying something tastes good. If you find something to be \
            delicious, you could simply say “Yummy!” or you could expand it into a sentence. This cheesecake \
            is really yummy. I’m going for another slice. Flavorful This is a great adjective for describing \
            food that’s full of flavor or that has a delicious quality in its taste and smell".split(' ')
    
    def get_review(self):
        words = self.words
        # generate a random review lenght
        review_length = random.randint(20, 40)
        # generate a random review rating
        rating = random.randint(1,5)

        word_idx = random.sample(range(0, len(words)-1), review_length)
        res = ''
        for i in word_idx:
            res += words[i]
            res += ' '
        
        return rating, res



        