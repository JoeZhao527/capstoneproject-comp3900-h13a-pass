from server import app
from flask import render_template, request
from backend.auth import *
from backend.schedule import *
from backend.data_access import *
from backend.voucher import *
import json

@app.route('/')
def home():
    return render_template('eatery_home.html')

@app.route('/diner/home')
def diner_home_load():
    return render_template('diner_home.html')

@app.route('/diner/register')
def diner_register_load():
    return render_template('diner_register.html')

@app.route('/diner/private_profile')
def diner_private_profile_load():
    return render_template('diner_profile.html')


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

@app.route('/reset_pass', methods=['GET'])
def reset_pass_page():
    return render_template('reset_pass.html')

@app.route('/reset_pass', methods=['POST'])
def reset_pass_send_email():
    email = request.data.decode('ascii')
    try:
        auth_password_request(email=email)
    except InputError:
        return 'failed'
    return ''

@app.route('/reset_pass', methods=['PUT'])
def reset_pass():
    data = json.loads(request.data)
    try:
        auth_password_reset(data['code'], data['new_pass'])
        return ''
    except InputError:
        return 'reset failed'

@app.route('/logout', methods=['PUT'])
def eatery_logout():
    data = json.loads(request.data)
    res = auth_logout(data['token'])
    return 'true' if res['logout_success'] else ''

@app.route('/eatery/register', methods=['POST'])
def eatery_register_check():
    data = json.loads(request.data)
    try:
        res = eatery_register(data['email'], data['password'],
                            data['fname'], data['lname'],data['phone'],
                            data['ename'], data['address'], data['menu'],
                            data['cuisines'], data['description'])
        return res['token']
    except InputError:
        print(InputError.message)
        return ''

@app.route('/diner/register', methods=['POST'])
def diner_register_check():
    data = json.loads(request.data)
    try:
        res = eatery_register(data['email'], data['password'],
                            data['fname'], data['lname'],data['phone'],
                            data['ename'])
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
    return json.dumps(res)

@app.route('/eatery_private_profile/update', methods=['PUT'])
def eatery_private_profile_update():
    data = json.loads(request.data)
    print(data)
    print('got')
    try:
        res = eatery_profile_update(data['token'], data['first_name'], data['last_name'],data['phone'],
                            data['eatery_name'], data['address'], data['menu'],
                            data['cuisines'], data['description'])
        return ''
    except InputError:
        return 'failed'
    
@app.route('/eatery_private_profile/add_schedule', methods=['POST'])
def eatery_add_schedule():
    print(request.data)
    info = json.loads(request.data)
    token = info['token']
    eatery_id = get_eatery_id(token)
    try:
        res = add_schedule(token=token, eatery_id=eatery_id, 
                        no_vouchers=info['schedule-amount'], weekday=info['weekday'],
                        start=info['schedule-start'], end=info['schedule-end'], 
                        discount=info['schedule-discount'])
        return str(res['schedule_id'])
    except InputError:
        return ''

@app.route('/eatery/profile/update_schedule', methods=['PUT'])
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
            return ''

    return render_template()

@app.route('/eatery/profile/remove_schedule', methods=['DELETE'])
def eatery_delete_schedule():
    print('delete schedule')
    try:
        info = json.loads(request.data)
        remove_schedule(token=info['token'], schedule_id=info['id'])
        return ''
    except InputError:
        print(InputError.message)
        return 'failed'

@app.route('/eatery/profile/remove_voucher', methods=["DELETE"])
def eatery_delete_voucher():
    print('delete voucher')
    try:
        info = json.loads(request.data)
        delete_voucher(token=info['token'], voucher_id=info['id'])
        return ''
    except InputError:
        print(InputError.message)
        return 'failed'

@app.route('/eatery/profile/get_schedule', methods=['POST'])
def eatery_get_schedule():
    data = json.loads(request.data)
    token = data['token']
    res = get_eatery_schedule(token)
    return json.dumps(res)

@app.route('/eatery/profile/get_voucher', methods=['POST'])
def eatery_get_voucher():
    data = json.loads(request.data)
    token = data['token']
    res = get_eatery_voucher(token)
    print(res)
    return json.dumps(res)