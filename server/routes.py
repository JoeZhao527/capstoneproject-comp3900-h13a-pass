from server import app
from flask import render_template, request
from backend.auth import *
from backend.schedule import *

import json

@app.route('/')
def home():
    return render_template('eatery_home.html')

@app.route('/eatery/register')
def eatery_register_load():
    return render_template('eatery_register.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_info():
    data = json.loads(request.data)
    try:
        res = auth_login(data['email'], data['password'])
        return res['token']
    except InputError:
        print(InputError.message)
        return ''

@app.route('/logout', methods=['PUT'])
def eatery_logout():
    data = json.loads(request.data)
    res = auth_logout(data['token'])
    return 'true' if res['logout_success'] else ''

@app.route('/eatery/register', methods=['POST'])
def eatery_register_check():
    print(request.data)
    data = json.loads(request.data)
    try:
        res = eatery_register(data['email'], data['password'],
                            data['fname'], data['lname'],data['phone'],
                            data['ename'], data['address'], data['menu'],
                            data['description'])
        return res['token']
    except InputError:
        print(InputError.message)
        return ''
        
@app.route('/eatery_private_profile', methods=['GET'])
def eatery_private_profile():
    return render_template('eatery_private_profile.html')

@app.route('/eatery_private_profile/info', methods=['POST'])
def eatery_private_profile_info():
    data = json.loads(request.data)
    res = get_eatery_by_token(data['token'])
    # returns json string if res is not empty, otherwise returns an empty string
    print(res)
    return json.dumps(res)

    
@app.route('/eatery/profile/private/add_schedule', methods=['POST'])
def eatery_add_schedule():
    info = json.loads(request.data)
    try:
        res = add_schedule(token=info['token'], eatery_id=info['eatery_id'], 
                        voucher_num=info['voucher_num'], weekday=info['weekday'],
                        start=info['start'], end=info['end'], 
                        discount=info['discount'], meal_type=info['meal_type']) 
        return res['schedule_id']
    except InputError:
        print(InputError.message)
        return ''

@app.route('/eatery/profile/update_schedule', methods=['GET', 'PUT'])
def eatery_update_schedule():
    if request.method == 'PUT':
        try:
            info = json.loads(request.data)
            schedule = update_schedule(token=info['token'], weekday=info['weekday'], 
                                    start=info['start'], end=info['end'],
                                    discount=info['discount'], voucher_num=info['voucher_num'],
                                    eatery_id=info['eatery_id'], schedule_id=info['schedule_id'],
                                    meal_type=info['meal_type']) 
            return schedule
        except InputError:
            print(InputError.message)
            return ''

    return render_template()

@app.route('/eatery/profile/remove_schedule', methods=['DELETE'])
def eatery_delete_schedule():
    try:
        info = json.loads(request.data)
        remove_schedule(token=info['token'], weekday=info['weekday'], 
                        eatery_id=info['eatery_id'], schedule_id=info['schedule_id'])
        print(info)
        return {}
    except InputError:
        print(InputError.message)
        return ''