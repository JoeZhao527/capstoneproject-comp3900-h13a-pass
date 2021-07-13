from flask import Response
from werkzeug.utils import redirect
from server import app
from flask import render_template, request, redirect
from backend.auth import *
from backend.schedule import *
from backend.data_access import *
from backend.voucher import *
from backend.image import *
import json

###########################################################
##                   COMMON ROUTES                       ##
###########################################################
@app.route('/')
def home():
    return redirect('/eatery/home', code=302)

@app.route('/logout', methods=['PUT'])
def eatery_logout():
    data = json.loads(request.data)
    res = auth_logout(data['token'])
    return 'true' if res['logout_success'] else ''

###########################################################
##                   DINER  ROUTES                       ##
###########################################################
@app.route('/diner/home')
def diner_home_load():
    return render_template('diner_home.html')

@app.route('/diner/register')
def diner_register_load():
    return render_template('diner_register.html')

@app.route('/diner/register', methods=['POST'])
def diner_register_check():
    data = json.loads(request.data)
    print(data)
    try:
        res = diner_register(data['email'], data['password'],
                            data['fname'], data['lname'],data['phone'])
        return json.dumps(res)
    except InputError:
        print(InputError.message)
        return ''

@app.route('/diner/private_profile')
def diner_private_profile_load():
    return render_template('diner_profile.html')

@app.route('/diner/login', methods=['POST'])
def diner_login_info():
    data = json.loads(request.data)
    print(data)
    try:
        res = diner_login(data['email'], data['password'])
        print(res)
        return json.dumps(res)
    except InputError:
        print(InputError.message)
        return ''
@app.route('/diner/home/getEatery',methods=['GET'])
def diner_getEatery():
    try:
        return json.dumps(get_num_eatery())
    except:
        return ''

###########################################################
##                   EATERY ROUTES                       ##
###########################################################

################# EATERY AUTHENTICATION ###################
@app.route('/eatery/home')
def eatery_home():
    return render_template('eatery_home.html')

@app.route('/eatery/register')
def eatery_register_load():
    return render_template('eatery_register.html')

@app.route('/eatery/login', methods=['POST'])
def eatery_login_info():
    data = json.loads(request.data)
    try:
        res = eatery_login(data['email'], data['password'])
        print(res)
        return json.dumps(res)
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

@app.route('/eatery/register', methods=['POST'])
def eatery_register_check():
    data = json.loads(request.data)
    try:
        res = eatery_register(data['email'], data['password'],
                            data['fname'], data['lname'],data['phone'],
                            data['ename'], data['address'], data['menu'],
                            data['cuisines'], data['city'], data['suburb'],
                            data['description'])
        return json.dumps(res)
    except InputError:
        print(InputError.message)
        return ''

################# EATERY PRIVATE PROFILE ###################
@app.route('/eatery/profile/private', methods=['GET', 'POST'])
def eatery_private_profile():
    return render_template('eatery_private_profile.html')

@app.route('/eatery/profile/private/info', methods=['POST'])
def eatery_private_profile_info():
    data = json.loads(request.data)
    res = get_eatery_by_token(data['token'])
    # returns json string if res is not empty, otherwise returns an empty string
    return json.dumps(res)

@app.route('/eatery/profile/private/update', methods=['PUT'])
def eatery_private_profile_update():
    data = json.loads(request.data)
    try:
        res = eatery_profile_update(data['token'], data['first_name'], data['last_name'],data['phone'],
                            data['eatery_name'], data['address'], data['menu'], data['cuisines'], 
                            data['city'], data['suburb'] ,data['description'])
        return ''
    except InputError:
        return 'failed'
    
@app.route('/eatery/profile/private/add_schedule', methods=['POST'])
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
        return ''
    except InputError:
        return 'failed'

@app.route('/eatery/profile/private/add_voucher', methods=['POST'])
def eatery_add_voucher():
    print(request.data)
    info = json.loads(request.data)
    token = info['token']
    eatery_id = get_eatery_id(token)
    no_vouchers = int(info['voucher-amount'])
    try:
        res = []
        for i in range(no_vouchers):
            res.append(add_voucher(token=token, eatery_id=eatery_id, date=info['date'],
                        start=info['voucher-start'], end=info['voucher-end'], 
                        discount=info['voucher-discount']))
        return ''
    except InputError:
        return 'failed'

@app.route('/eatery/profile/private/update_schedule', methods=['PUT'])
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

@app.route('/eatery/profile/private/remove_schedule', methods=['DELETE'])
def eatery_delete_schedule():
    print('delete schedule')
    try:
        info = json.loads(request.data)
        for id in info['id']:
            remove_schedule(token=info['token'], schedule_id=id)
        return ''
    except InputError:
        print(InputError.message)
        return 'failed'

@app.route('/eatery/profile/private/remove_voucher', methods=["DELETE"])
def eatery_delete_voucher():
    print('delete voucher')
    try:
        info = json.loads(request.data)
        for id in info['id']:
            delete_voucher(token=info['token'], voucher_id=id)
        return ''
    except InputError:
        print(InputError.message)
        return 'failed'

@app.route('/eatery/profile/private/get_schedule', methods=['POST'])
def eatery_get_schedule():
    data = json.loads(request.data)
    token = data['token']
    res = get_eatery_schedule(token)
    return json.dumps(res)

@app.route('/eatery/profile/private/get_voucher', methods=['POST'])
def eatery_get_voucher():
    data = json.loads(request.data)
    token = data['token']
    res = get_eatery_voucher(token)
    print(res)
    return json.dumps(res)

@app.route('/eatery/profile/private/upload_image', methods=['POST'])
def eatery_upload_image():
    data = json.loads(request.data)
    try:
        image_id = upload_image(token=data['token'], img=data['image'])
        print(image_id)
        return ''
    except InputError:
        return 'failed'

@app.route('/eatery/profile/private/get_image', methods=['POST'])
def eatery_get_image():
    data = json.loads(request.data)
    token = data['token']
    res = get_eatery_image(token=token)
    return json.dumps({'data':res})

@app.route('/eatery/profile/private/delete_image', methods=['DELETE'])
def eatery_delete_image():
    try:
        info = json.loads(request.data)
        delete_image(token=info['token'], image_id=info['id'])
        return ''
    except InputError:
        print(InputError.message)
        return 'failed'

################ EATERY PUBLIC PROFILE ##################
@app.route('/eatery/profile/<int:id>', methods=['GET'])
def eatery_public_profile(id):
    return render_template('eatery_public_profile.html')

@app.route('/eatery/profile/<int:id>/get_image', methods=['GET'])
def eatery_public_get_image(id):
    try:
        return json.dumps({'data':get_image_by_id(id)})
    except InputError:
        return ''

@app.route('/eatery/profile/<int:id>/get_info', methods=['GET'])
def eatery_public_get_info(id):
    try:
        return json.dumps(get_eatery_by_id(id))
    except:
        return ''

@app.route('/eatery/profile/<int:id>/get_vouchers', methods=['GET'])
def eatery_public_get_voucher(id):
    try:
        return json.dumps(get_eatery_voucher(id))
    except:
        return  ''