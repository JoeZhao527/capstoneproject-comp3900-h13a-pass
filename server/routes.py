from server import app
from flask import render_template, request
from backend.auth import *
from backend.schedule import *
import json

@app.route('/')
def home():
    return render_template('eatery_home.html')

@app.route('/eatery/register')
def eatery_register():
    return render_template('eatery_register.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_info():
    data = json.loads(request.data)
    return data

@app.route('/eatery_private_profile', methods=['GET'])
def eatery_private_profile():
    return render_template('eatery_private_profile.html')

@app.route('/eatery/profile/private/add_schedule', methods=['POST'])
def eatery_add_schedule():
    info = json.loads(request.data)
    #success = add_schedule(token=info['token'], weekday=info['weekday'], discount_number=info['discount_number'], start=info['start'], end=info['end'], eatery_id=info['eatery_id']) 
    print(info)
    return '1'

@app.route('/eatery/profile/update_schedule', methods=['GET', 'PUT'])
def eatery_update_schedule():
    if request.method == 'PUT':
        info = json.loads(request.data)
        #schedule = update_schedule(token=info['token'], weekday=info['weekday'], discount_number=info['discount_number'], 
        #                        start=info['start'], end=info['end'], eatery_id=info['eatery_id']) 
        return schedule

    return render_template()

@app.route('/eatery/profile/remove_schedule', methods=['DELETE'])
def eatery_delete_schedule():
    info = json.loads(request.data)
    #success = remove_schedule(token=info['token'], weekday=info['weekday'], schedule_id=info['schedule_id'], eatery_id=info['eatery_id'])
    print(info)
    return 'true'