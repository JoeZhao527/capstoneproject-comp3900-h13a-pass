// path
const eatery_home = '/eatery/home'

// token and id
let token = sessionStorage.getItem('token');
let eatery_id = sessionStorage.getItem('id');
let utype = sessionStorage.getItem('utype');

// check if there's no token
function loadPage() {
    token = sessionStorage.getItem('token');
    console.log(token)
    if (typeof token === 'undefined' || token == null) {
        window.location.href = eatery_home;
    }
}

loadPage();

const home_btn = document.querySelector(".home");
home_btn.addEventListener('click', function() {
    window.location.href = eatery_home;
})

/* side bar swicth page logic */
const side_bar = document.getElementById('side-bar')
const switchs = side_bar.getElementsByTagName('div');
const pages = document.getElementsByClassName('page');

for (let i = 0; i < switchs.length; i++) {
    switchs[i].onclick = () => {
        displayPage(pages[i]);
        for (let j = 0; j < switchs.length; j++) {
            if (i === j) {
                switchs[j].style.boxShadow = '10px 10px 10px 10px rgba(0,0,0,0.05)'
            } else {
                switchs[j].style.boxShadow = 'none'
            }
        }
    }
}

function displayPage(page) {
    for (const p of pages) {
        if (p === page) {
            p.style.display = 'block'
            if (getCurrPage() === 'view-voucher') {private_loadVouchers();}
        } else {p.style.display = 'none'}
    }
}

displayPage(pages[0]);
switchs[0].style.boxShadow = '10px 10px 10px 10px rgba(0,0,0,0.05)';

/* logout button, logout logic in logout.js */
const logout_btn = document.getElementById('logout-btn');

/* go to eatery public page */


/* content */

// profile
const profile_form = document.getElementById('profile-form');
const profile_item = profile_form.getElementsByTagName('input');
let menu_input =  document.getElementById('menu');
let menu_link = document.getElementById('view-menu');
const menu_section = document.getElementById('menu-section');

// get eatery's info by its token
function getEateryData() {
    let _data = {}
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/info', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const [key, value] of Object.entries(JSON.parse(this.response))) {
                _data[key] = value;
            }
            loadEateryData(_data);
        }
    }
    xhr.send(`{"token":"${token}"}`);
}

// load eatery data to profile
function loadEateryData(data) {
    Array.from(profile_item).forEach(e => {
        if (e.name) {
            e.value = data[e.name]
        }
    });
    if(data['cuisine']) {loadCuisines(data['cuisine'].split(','))}
    menu_link.onclick = () => {
        let iframe
        if (data['menu']) {
            iframe = document.createElement('iframe');
            iframe.src = data['menu']
        } else {
            iframe = document.createElement('h1');
            iframe.innerHTML = "No menu is uploaded yet, click update profile to see the change"
        }
        menu_section.innerHTML = ''
        menu_section.appendChild(iframe)
        menu_section.style.display = 'inline';
    }
}

/* add cuisine */
const cuisines = []
const cuisine = document.getElementById('cuisine')
const add_cuisine_btn = document.getElementById('add-cuisine')
const cuisine_list = document.getElementById('cuisines');

add_cuisine_btn.addEventListener('click', function(e) {
    e.preventDefault();
    let cuisine = document.getElementById("cuisine");
    if(cuisine.value !== `` && cuisines.includes(cuisine.value) == false) {
        cuisine_list.appendChild(cuisineBtn(cuisine.value));
        cuisines.push(cuisine.value);
    }
    cuisine.value = ``;
});

function cuisineBtn(value) {
    let btn = document.createElement('button');
    btn.appendChild(document.createTextNode(value));
    cuisineListener(btn);
    return btn;
}

function cuisineListener(btn) {
    let context = btn.innerHTML
    btn.onclick = () => {
        cuisine_list.removeChild(btn);
        let idx = cuisines.indexOf(context);
        if (idx > -1) { cuisines.splice(idx, 1) }
    }

    btn.onmouseover = () => {
        btn.innerHTML = 'Delete';
    }

    btn.onmouseleave = () => {
        btn.innerHTML = context;
    }
}

function loadCuisines(c) {
    for (let i = 0; i < c.length; i++) {
        cuisine_list.appendChild(cuisineBtn(c[i]));
        cuisines.push(c[i])
    }
}

getEateryData();

/* update profile */
const update = document.getElementById('submit');

profile_form.onsubmit = (e) => {
    e.preventDefault();
    let data = {}
    Array.from(profile_form).forEach(e => {
        if(e.type !== `button` && e.type !== `submit` && e.type != 'file' && e.name) {
            data[e.name] = e.value;
        }
    });
    data['cuisines'] = cuisines.join(',');
    data['token'] = token;
    // menu
    if (typeof menu_input.files[0] == 'undefined') {
        data['menu'] = ''
        updateProfile(data)
    } else {
        if (isPDF(menu_input.files[0])) {
            let reader = new FileReader();
            reader.readAsDataURL(menu_input.files[0]);
            reader.onloadend = function () {
                data['menu'] = reader.result;
                updateProfile(data)
            }
        } else {
            let profile_update_err_msg = document.getElementById('profile-msg')
                profile_update_err_msg.innerHTML = "please upload pdf file less than 150Kb for menu only"
                profile_update_err_msg.style.color = 'red'
                setTimeout(() => {
                    profile_update_err_msg.innerHTML = ''
                }, 2000)
        }
    }
}

function isPDF(file) {
    if (typeof file == 'undefined') return true
    var fileName = file.name;
    var ext = fileName.substring(fileName.lastIndexOf('.') + 1);
    if (ext == 'pdf' && file.size < 150000) return true;
    else return false;
}

function updateProfile(data) {
    // send data and receive token
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/eatery/profile/private/update', false);
    xhr.send(JSON.stringify(data))
    if (!xhr.result) {
        update.style.backgroundColor = 'green';
        update.value = 'Profile is successfully updated!'
        setTimeout(() => {
            update.style.backgroundColor = '#2691d9';
            update.value = 'Update Profile'
            location.reload();
        }, 2000)
    } else {
        let profile_update_err_msg = document.getElementById('profile-msg')
        profile_update_err_msg.innerHTML = "updated profile contains invalid information, failed to update"
        profile_update_err_msg.style.color = 'red'
        setTimeout(() => {
            profile_update_err_msg.innerHTML = ''
        }, 2000)
    }
}

/* add item */
/**
 * 
 * @param {*} data data of schedule/voucher Item, include time, weekday, discount etc.
 * @param {*} id group_id for voucher, schedule_id for schedule
 * @param {*} addDelete add deletebutton function. the id will be used to delete schedule/vouchers
 * @returns returns a voucehr/schedule item that can be append to voucher/schedule table
 */
function createItem(data, id, addDeleteAll) {
    let item = document.createElement('tr');
    for (const [key, value] of Object.entries(data)) {
        const hidden_attr = ['token', 'id', 'eatery_id', 'diner_id', 'if_used', 'if_booked', 'code', 'group_id', 'amount']
        if (!hidden_attr.includes(key)) {
            let td = document.createElement('td');
            td.appendChild(document.createTextNode(value));
            item.appendChild(td);
        }
    }
    // only voucher has date, use this to check the type of node
    let num_voucher = data['amount']
    if ('date' in data) {
        let td = document.createElement('td');
        td.appendChild(document.createTextNode(num_voucher));
        item.appendChild(td);
    }

    addDeleteAll(item, id);
    return item;
}

function createVoucherItem(data, id) {
    let item = document.createElement('tr');
    for (const [key, value] of Object.entries(data)) {
        const hidden_attr = [
            'token', 'id', 'eatery_id', 'diner_id', 'if_used', 
            'if_booked', 'code', 'group_id', 'amount', 
            'arrival_time', 'num_of_guest', 'special_request',
            'schedule_id'
        ]
        if (!hidden_attr.includes(key)) {
            let td = document.createElement('td');
            td.appendChild(document.createTextNode(value));
            item.appendChild(td);
        }
    }

    let td = document.createElement('td');
    td.appendChild(document.createTextNode(data['amount']));
    item.appendChild(td);

    addDeleteVoucherBtn(item, id);
    return item;
}

function mapWeekday(n) {
    const weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return weekday[n]
}

/* add schedule */
const add_schedule_btn = document.getElementById('add-schedule-btn');   // add schedule button in view schedule
const add_schedule_page = document.getElementById('add-schedule');      // subpage container
const schedule_form = document.getElementById('schedule-form');         // form in subpage
const schedule_elem = schedule_form.elements;                           // form elements
const schedule_submit = document.getElementById('submit-schedule');     // submit button in subpage
const schedules = document.getElementById('schedules')                  // schedules table
let schedule_data = {}

// open add schedule page
add_schedule_btn.onclick = () => {
    add_schedule_page.style.display = 'inline';
};



schedule_form.onsubmit = (e) => {
    e.preventDefault();
    Array.from(schedule_elem).forEach(function(e) {
        if (e.type !== 'submit') {
            schedule_data[e.id] = e.value;
        }
    })
    schedule_data['token'] = sessionStorage.getItem('token');
    addScheduleREquest(schedule_data);
    schedule_form.reset();
    add_schedule_page.display = 'none';
    schedule_data = {};
}

function addScheduleREquest(data) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/add_schedule', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (!this.response) {
                loadSchedules();
            }
            else {
                document.getElementById('schedule-msg').innerHTML = 'invaild schedule';
                setTimeout(() => {
                    document.getElementById('schedule-msg').innerHTML = '';
                }, 2000);
            }
        }
    }
    xhr.send(JSON.stringify(data));
}

function addScheduleItem(data, id) {
    schedules.appendChild(createItem(data,id,addDeleteScheduleBtn));
}

function addDeleteScheduleBtn(item, id) {
    let btn = document.createElement('button');
    btn.className = 'delete'
    btn.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/eatery/profile/private/remove_schedule', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ token: token, id: id }));
        if (!this.response) {
            schedules.removeChild(item);
        } else {
            alert('delete failed');
        }
    }
    item.appendChild(btn);
}

function loadSchedules() {
    clearSchedules();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/get_schedule', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const data of JSON.parse(this.response)['schedules']) {
                addScheduleItem(data, data['id']);
            }
        }
    }
    xhr.send(JSON.stringify({ token:token }))
    // add data to schedule list
}

function clearSchedules() {
    schedules.innerHTML = '<tr class="th"><th>weekday</th><th>start</th><th>end</th><th>discount</th><th>amount</th><th>Actions</th></tr>'
}

loadSchedules();


/* add voucher */
const add_voucher_btn = document.getElementById('add-voucher-btn');
const add_voucher_page = document.getElementById('add-voucher');
const voucher_form = document.getElementById('voucher-form');
const voucher_elem = voucher_form.elements;
const voucher_submit = document.getElementById('submit-voucher');
const vouchers = document.getElementById('vouchers');
let voucher_data = {}
let voucher_list = []
// open add voucher page
add_voucher_btn.onclick = () => {
    add_voucher_page.style.display = 'inline';
};

voucher_form.onsubmit = (e) => {
    e.preventDefault();
    Array.from(voucher_elem).forEach(function(e) {
        if (e.type !== 'submit') {
            voucher_data[e.id] = e.value;
        }
    })
    voucher_data['token'] = sessionStorage.getItem('token');
    addVoucherRequest(voucher_data);
    voucher_form.reset();
    add_voucher_page.display = 'none';
    voucher_data = {};
}

function addVoucherRequest(data) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/add_voucher', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (!this.response) {
                private_loadVouchers();
            } else {
                document.getElementById('voucher-msg').innerHTML = 'invaild voucher';
                setTimeout(() => {
                    document.getElementById('voucher-msg').innerHTML = '';
                }, 2000);
            }
        }
    }
    xhr.send(JSON.stringify(data));
}

/**
 * this will be called by private_loadVouchers in load_vouchers.js
 * @param data voucher's data, include date, start/end time, discount and amount
 * @param id voucher's group_id, which can be used to add/delete voucher
 */
function addVoucherItem(data, id) {
    // creatItem create a voucher
    vouchers.appendChild(createVoucherItem(data, id));
}

/**
 * add a delete button to a voucher item, which will delete all vouchers by its group_id
 */
function addDeleteVoucherBtn(item, id) {
    let delete_all = document.createElement('button');
    delete_all.className = 'delete';
    delete_all.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/eatery/profile/private/delete_all_vouchers', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ token: token, id: id }));
        if (!this.response) {
            vouchers.removeChild(item);
        } else {
            alert('delete failed');
        }
    }
    item.appendChild(delete_all);
}

// close subpage
document.onmousedown = (e) => {
    if (getCurrPage() === 'view-voucher') {
        if ((!add_voucher_page.contains(e.target)) && 
            add_voucher_page.style.display === 'inline'&&
            (!add_voucher_btn.contains(e.target))) {
            add_voucher_page.style.display = 'none';
        }
    } else if (getCurrPage() === 'view-schedule'){
        if ((!add_schedule_page.contains(e.target)) && 
            add_schedule_page.style.display === 'inline'&&
            (!add_schedule_btn.contains(e.target))) {
            add_schedule_page.style.display = 'none';
        }
    } else if (getCurrPage() === 'view-reservation') {
        if ((!checkcode_page.contains(e.target)) && 
            checkcode_page.style.display === 'inline') {
            checkcode_page.style.display = 'none';
        } else if ((!view_detail_page.contains(e.target) && 
            view_detail_page.style.display === 'inline') ||
            close_view_detail_btn.contains(e.target)) {
            view_detail_page.style.display = 'none';
        } else if ((!view_review_page.contains(e.target)) && 
            view_review_page.style.display === 'inline') {
            view_review_page.style.display = 'none';
        }
    } else if (getCurrPage() === 'profile') {
        if (!(menu_section.contains(e.target) &&
            menu_section.style.display == 'inline')) {
            menu_section.style.display = 'none';
        }
    }
}

// get the current active page
function getCurrPage() {
    for (const p of pages) {
        if (p.style.display === 'block') {return p.id;}
    }
}


const input = document.getElementById('image');
const image_box = document.getElementById('image-container');
const image_msg = document.getElementById('image-msg');
input.addEventListener('change', handleFiles, false);

function handleFiles(e) {
    if (isImage(e.target.files[0])) {
        let reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]);
        reader.onloadend = function () {
            let data = { token: token, image: reader.result }
            let xhr = new XMLHttpRequest();
            xhr.open('POST', '/eatery/profile/private/upload_image', true);
            xhr.setRequestHeader('Content-Type', 'application/json')
            xhr.onreadystatechange = () => {
                if (this.readyState == 4 && this.status == 200) {
                    if (!this.response) {
                        load_image();
                    } else {
                        image_msg.innerHTML = 'image failed to upload, try another one'
                        setTimeout(() => {
                            image_msg.innerHTML = ''
                        }, 2000)
                    }
                }
            }
            xhr.send(JSON.stringify(data));
        }
    } else {
        image_msg.innerHTML = 'please upload .png and .jpeg only!'
        setTimeout(() => {
            image_msg.innerHTML = ''
        }, 2000)
    }
}

function isImage(file) {
    const acceptedImageTypes = ['image/jpeg', 'image/png'];
    return file && acceptedImageTypes.includes(file['type'])
}


function load_image() {
    image_box.innerHTML = ''
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/get_image', true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let image_list = JSON.parse(this.response)['data']
            for(const item of image_list) {
                let div =createImage(item['image'], item['id'])
                image_box.appendChild(div);
            }
        }
    }
    xhr.send(JSON.stringify({token:token}))
}

function createImage(src, img_id) {
    // container for delete button and image
    let div = document.createElement('div');
    // image
    let img = new Image();
    img.src = src;
    // button
    let btn = document.createElement('button');
    btn.innerHTML = 'delete'
    btn.onclick = () => {
        deleteImage(token, img_id, div)
    }
    div.appendChild(img);
    div.appendChild(btn);
    return div
}

function deleteImage(token, id, div) {
    let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/eatery/profile/private/delete_image', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ token: token, id: id }));
        if (!this.response) {
            image_box.removeChild(div);
        } else {
            alert('delete failed');
        }
}

load_image();

/* got to public profile */
const preview_btn = document.getElementById('preview-btn');

preview_btn.onclick = () => {
    window.location.href = `/eatery/profile/${eatery_id}`
}