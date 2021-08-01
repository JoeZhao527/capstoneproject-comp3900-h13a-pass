# crutial import for backend to run py itself
import os, sys
from re import sub
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from backend.user_db import *
from backend.auth import *
from datetime import date, timedelta
from backend.voucher import convert_string_to_time, weekdays
import random

from .progression_bar import printProgressBar
import time as _time

# load vouchers for m eateries, n diners
def load_voucher(m, n):

    # for each eatery
    gid = 1000
    printProgressBar(0, n, prefix = 'Progress:', suffix = '', length = 50)
    for eid in range(0,m):
        _time.sleep(0.1)
        # 3 days in future, 4 days in past
        dl = Date().get_dates(3,4)
        v_data = []
        # for each date in the random date list
        for d in dl:
            # generate a random time period list
            tl = Time().get_times()
            # for each time period in the time period list
            for t in tl:
                # combine date and time, append to voucher data list
                mix = string.ascii_letters + string.digits
                code = ''.join(random.choice(mix) for i in range(20))
                discount = random.randint(10,90)
                v_data.append(d + t + (discount, code, gid))
                gid += 1
        for data in v_data:
            # voucher number of the vouchers with same group id
            num = random.randint(2,8)
            diner_list = random.sample(range(1,n), num//2)
            for _ in range(num):
                # data[1]: date, data[1]: weekday, data[2]: start_time, data[3]:end_time, data[4]:discount
                # data[5]: code, data[6]: gid
                voucher = Voucher(eid, data[0],data[2], data[3], data[4], data[5], data[6])
                voucher.weekday = weekdays[data[1]]

                if diner_list:
                    diner = diner_list.pop()
                else:
                    diner = None
                
                if diner:
                    used = random.randint(0,1)
                    voucher.diner_id = diner
                    voucher.if_used = False if used == 0 else True
                    voucher.if_booked = True
                    voucher.arrival_time = time(10,30)
                    voucher.num_of_guest = random.randint(3,6)
                    voucher.special_request = "A long string to test view special request functionailty\
                            A long string to test view special request functionailty\
                            A long string to test view special request functionailty"
                else:
                    voucher.diner_id = None
                    voucher.if_used = False
                    voucher.if_booked = False

                
                db.session.add(voucher)
                db.session.commit()
        printProgressBar(eid + 1, m, prefix = 'Loading Vouchers:', suffix = '', length = 50)
    pass

class Date:
    def __init__(self) -> None:
        self.today = date.today()

    def get_future(self, n):
        # generate a random list of n days, n less than 6
        n = min(n, 6)
        rl = random.sample(range(1,6), n)
        res = []
        for i in rl:
            today = self.today + timedelta(days=i)
            day = today.weekday()
            res.append((today, day))
        return res
    
    def get_past(self, n):
        n = min(n, 7)
        rl = random.sample(range(0,6), n)
        res = []
        for i in rl:
            today = self.today - timedelta(days=i)
            day = today.weekday()
            res.append((today, day))
        return res
    
    def get_dates(self, m, n):
        get_future = self.get_future(m)
        get_past = self.get_past(n)
        return get_past + get_future

class Time:
    def __init__(self) -> None:
        self.times = [
            ['05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30'],
            ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30'],
            ['15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30'],
            ['22:00', '22:30', '23:00', '23:30', '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30']
        ]
    
    # return a list of tuples, each tuple has (start_time, end_time)
    def get_times(self):
        times = self.times
        ri = random.randint(0,3)
        rl = random.sample(range(0,3), ri)
        res = []
        for i in rl:
            time = times[i]
            mid = len(time)//2
            start = time[random.randint(0, mid)]
            end = time[random.randint(mid+1, len(time)-1)]
            start = convert_string_to_time(start)
            end = convert_string_to_time(end)
            res.append((start,end))
        return res
