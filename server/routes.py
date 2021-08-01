from flask import Response
from werkzeug.utils import redirect
from server import app
from flask import render_template, request, redirect
from backend.auth import *
from backend.schedule import *
from backend.data_access import *
from backend.voucher import *
from backend.image import *
from backend.diner import *
import json

###########################################################
##                   COMMON ROUTES                       ##
###########################################################
@app.route('/')
def home():
    return redirect('/diner/home', code=302)

@app.route('/logout', methods=['PUT'])
def eatery_logout():
    data = json.loads(request.data)
    res = auth_logout(data['token'])
    return 'true' if res['logout_success'] else ''

@app.route('/search', methods=['POST'])
def search_eatery_by_key():
    keyword = json.loads(request.data)['keyword']
    res = search_by_key(keyword)
    return json.dumps({'data':res})

###########################################################
##                   DINER  ROUTES                       ##
###########################################################
@app.route('/diner/home')
def diner_home_load():
    update_voucher_by_schedule()
    return render_template('home.html')

@app.route('/diner/register')
def diner_register_load():
    return render_template('diner_register.html')

@app.route('/diner/register', methods=['POST'])
def diner_register_check():
    data = json.loads(request.data)
    try:
        res = diner_register(data['email'], data['password'],
                            data['fname'], data['lname'],data['phone'])
        return json.dumps(res)
    except InputError as e:
        return e.message

@app.route('/diner/login', methods=['POST'])
def diner_login_info():
    data = json.loads(request.data)
    try:
        res = diner_login(data['email'], data['password'])
        return json.dumps(res)
    except InputError:
        return ''

@app.route('/diner/home/get_location', methods=['GET'])
def get_location_list():
    return json.dumps(suburb_with_city())

@app.route('/diner/home/get_cuisine', methods=['GET'])
def get_cuisine_list():
    return json.dumps(cuisine_of_eateries())

@app.route('/diner/get_eatery', methods=['POST'])
def get_eatery_list():
    data = json.loads(request.data)
    _date = data['date']
    _time = data['time']
    location = data['location']
    cuisine = data['cuisine']
    try:
        res = search_by_filter(_date, _time, location, cuisine)
        return json.dumps({'eateries':res})
    except InputError:
        return ''

@app.route('/diner/get_eatery/recommend', methods=['POST'])
def get_eatery_recommendation():
    token = json.loads(request.data)['token']
    try:
        res = get_recommendations(token)
        return json.dumps({'eateries':res})
    except InputError:
        return ''
@app.route('/diner/home/getEatery',methods=['GET'])
def diner_getEatery():
    try:
        data = get_all_eatery()
        return json.dumps(data)
    except:
        return ''

@app.route('/diner/profile/private', methods=['GET'])
def diner_private_profile():
    return render_template('diner_profile.html')

@app.route('/diner/profile/private/info', methods=['POST'])
def diner_private_profile_info():
    data = json.loads(request.data)
    res = get_diner_by_token(data['token'])
    # returns json string if res is not empty, otherwise returns an empty string
    return json.dumps(res)

@app.route('/diner_private_profile/update', methods=['PUT'])
def diner_private_profile_update():
    data = json.loads(request.data)
    try:
        res = diner_profile_update(data['token'], data['first_name'], data['last_name'],data['phone'])
        return ''
    except InputError:
        return 'failed'

@app.route('/diner/profile/get_active',methods = ['POST'])
def diner_profile_active():
    data = json.loads(request.data)
    res = get_booked_voucher(data['token'])
    return json.dumps(res)
    

@app.route('/diner/profile/get_previous',methods = ['POST'])
def diner_profile_previous():
    data = json.loads(request.data)
    res = get_used_voucher(data['token'])
    return json.dumps(res)

@app.route('/diner/profile/get_expired',methods = ['POST'])
def diner_profile_expired():
    data = json.loads(request.data)
    res = diner_get_booked_expired_voucher(data['token'])
    return json.dumps(res)

@app.route('/diner/profile/private/delete_voucher', methods=["DELETE"])
def diner_profile_deleate_voucher():
    try:
        info = json.loads(request.data)
        cancel_voucher(token=info['token'], voucher_id=info['id'])
        return ''
    except InputError:
        return 'failed'

@app.route('/diner/profile/add_review', methods=['POST'])
def diner_add_comment():
    data = json.loads(request.data)
    token, voucher_id, comment, rating = data['token'], data['voucher_id'], data['comment'], data['rating']
    try:
        add_review(token, voucher_id, comment, rating)
        return ''
    except:
        return 'failed'


###########################################################
##                   EATERY ROUTES                       ##
###########################################################

################# EATERY AUTHENTICATION ###################
@app.route('/eatery/home')
def eatery_home():
    update_voucher_by_schedule()
    return render_template('eatery_home.html')

@app.route('/eatery/register')
def eatery_register_load():
    return render_template('eatery_register.html')

@app.route('/eatery/login', methods=['POST'])
def eatery_login_info():
    data = json.loads(request.data)
    try:
        res = eatery_login(data['email'], data['password'])
        return json.dumps(res)
    except InputError:
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
    except InputError as e:
        return e.message

################# EATERY PRIVATE PROFILE ###################
@app.route('/eatery/profile/private', methods=['GET'])
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
    try:
        info = json.loads(request.data)
        remove_schedule(token=info['token'], schedule_id=info['id'])
        return ''
    except InputError:
        return 'failed'

@app.route('/eatery/profile/private/delete_all_vouchers', methods=["DELETE"])
def eatery_delete_voucher():
    try:
        info = json.loads(request.data)
        delete_all_vouchers(token=info['token'], group_id=info['id'])
        return ''
    except InputError:
        return 'failed'

@app.route('/eatery/profile/private/delete_voucher_by_id', methods=['DELETE'])
def eatery_delete_expired_reservation():
    try:
        info = json.loads(request.data)
        delete_voucher_by_id(info['token'], info['voucher_id'])
        return ''
    except InputError:
        return 'failed'
        
@app.route('/eatery/profile/private/get_schedule', methods=['POST'])
def eatery_get_schedule():
    data = json.loads(request.data)
    token = data['token']
    res = get_eatery_schedule(token)
    return json.dumps(res)

@app.route('/eatery/profile/private/get_voucher', methods=['POST'])
def eatery_get_voucher():
    update_voucher_by_schedule()
    data = json.loads(request.data)
    token = data['token']
    res = get_unbooked_voucher(token)
    return json.dumps(res)

@app.route('/eatery/profile/private/get_reservation/<filter>', methods=['POST'])
def eatery_get_all_reservation(filter):
    data = json.loads(request.data)
    token = data['token']
    sort_method = data['sort_method']
    sort_reverse = data['sort_reverse']
    try:
        # get result voucher list by filter type
        if filter == 'all':
            res = get_all_diner_voucher(token)
        elif filter == 'expired':
            res = get_booked_expired_voucher(token)
        elif filter == 'incomplete':
            res = get_booked_diner_voucher(token)
        elif filter == 'completed':
            res = get_booked_used_voucher(token)

        # sort result voucher list by sort method
        if sort_method == 'by time':
            res['vouchers'] = sorted(res['vouchers'], key=lambda k: (k['date'], k['start_time']), reverse=sort_reverse)
        elif sort_method == 'by discount':
            res['vouchers'] = sorted(res['vouchers'], key=lambda k: (k['discount']), reverse=sort_reverse)
        return json.dumps(res)
    except InputError:
        return ''

@app.route('/eatery/profile/private/complete_booking', methods=['POST'])
def eatery_complete_booking():
    data = json.loads(request.data)
    token = data['token']
    voucher_id = data['voucher_id']
    try:
        complete_booking(token, voucher_id)
        return ''
    except InputError:
        return 'failed'

@app.route('/eatery/profile/private/upload_image', methods=['POST'])
def eatery_upload_image():
    data = json.loads(request.data)
    try:
        image_id = upload_image(token=data['token'], img=data['image'])
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
        return 'failed'

@app.route('/eatery/profile/private/get_analytic', methods=['POST'])
def eatery_get_analytic():
    try:
        token = json.loads(request.data)['token']
        res = get_analytic(token)
        return json.dumps(res)
    except InputError:
        return ''
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
    update_voucher_by_schedule()
    try:
        res = json.dumps(get_unbooked_voucher(id))
        return res
    except:
        return  ''

@app.route('/eatery/profile/<int:id>/book_voucher', methods=['POST'])
def diner_book_voucher(id):
    data = json.loads(request.data)
    arrival_time = data['arrival_time']
    num_people = data['number_of_people']
    additional_request = data['request']
    try:
        book_voucher(data['token'], data['group_id'], arrival_time, num_people, additional_request)
        return ''
    except InputError:
        return 'failed'

@app.route('/eatery/profile/<int:id>/get_reviews', methods=['POST'])
def eatery_public_get_reviews(id):
    sort_order = json.loads(request.data)['sort']
    try:
        res = read_reviews(id)
        # sort order '1' for postive first, '0' for negative first
        if sort_order == '1':
            res['reviews'] = sorted(res['reviews'], key=lambda k: (k['rating']), reverse=True)
        else:
            res['reviews'] = sorted(res['reviews'], key=lambda k: (k['rating']), reverse=False)
        return json.dumps(res)
    except:
        return ''