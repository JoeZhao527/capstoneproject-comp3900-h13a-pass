// path
const eatery_home = '/'

// token
let token = sessionStorage.getItem('token');

/* side bar swicth page logic */
const side_bar = document.getElementById('side-bar')
const switchs = side_bar.getElementsByTagName('div');
const pages = document.getElementsByClassName('page');

for (let i = 0; i < switchs.length; i++) {
    switchs[i].onclick = () => {
        displayPage(pages[i]);
    }
}

function displayPage(page) {
    for (const p of pages) {
        if (p === page) {p.style.display = 'block'}
        else {p.style.display = 'none'}
    }
}

displayPage(pages[0]);

/* logout */
const logout_btn = document.getElementById('logout');

logout_btn.onclick = () => {
    if (logout()) {
        sessionStorage.removeItem('token');
        window.location.href = eatery_home;
    } else {
        alert('logout failed');
    }
}

/**
 * send logout request to backend
 */
 function logout() {
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/logout', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(`{"token":"${token}"}`);
    console.log(xhr.response);
    return xhr.response
}

/* content */

// profile
const profile_form = document.getElementById('profile-form');
const profile_item = profile_form.getElementsByTagName('input');

// get eatery's info by its token
function getEateryData() {
    let _data = {}
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery_private_profile/info', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const [key, value] of Object.entries(JSON.parse(this.response))) {
                _data[key] = value;
            }
            console.log(_data);
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
    console.log(data, data['cuisine'])
    if(data['cuisine']) {loadCuisines(data['cuisine'].split(','))}
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
    console.log(cuisines)
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
    console.log(profile_form)
    Array.from(profile_form).forEach(e => {
        if(e.type !== `button` && e.type !== `submit` && e.name) {
            data[e.name] = e.value;
        }
    });
    data['cuisines'] = cuisines.join(',');
    data['token'] = token;
    // menu
    data['menu'] = ''
    console.log(data)
    if (updateProfile(data) === '') {
        console.log('success')
    } else {
        alert('sign up failed')
    }
}

function updateProfile(data) {
    // send data and receive token
    console.log(data)
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/eatery_private_profile/update', false);
    xhr.send(JSON.stringify(data))
    console.log('here');
    return xhr.response;
}

/* add item */
function createItem(data, id, addDelete) {
    let item = document.createElement('tr');
    for (const [key, value] of Object.entries(data)) {
        const hidden_attr = ['token', 'id', 'eatery_id', 'diner_id', 'if_used', 'if_booked', 'code']
        if (!hidden_attr.includes(key)) {
            console.log(key, value, typeof value);
            let td = document.createElement('td');
            td.appendChild(document.createTextNode(value));
            item.appendChild(td);
        }
    }
    addDelete(item, id);
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
    xhr.open('POST', '/eatery_private_profile/add_schedule', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            addScheduleItem(data, parseInt(this.response));
        }
    }
    xhr.send(JSON.stringify(data));
}

function addScheduleItem(data, id) {
    schedules.appendChild(createItem(data,id,addDeleteScheduleBtn));
}

function addDeleteScheduleBtn(item, id) {
    let btn = document.createElement('button');
    btn.innerHTML = 'Delete';
    btn.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/eatery/profile/remove_schedule', false);
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
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/get_schedule', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const data of JSON.parse(this.response)['schedules']) {
                addScheduleItem(data, data['id']);
            }
        }
    }
    xhr.send(`{ "token":"${token}" }`)
    // add data to schedule list
}

loadSchedules();


/* add voucher */
const add_voucher_btn = document.getElementById('add-voucher-btn');
const add_voucher_page = document.getElementById('add-voucher');
const voucher_form = document.getElementById('voucher-form');
const voucher_elem = voucher_form.elements;
const voucher_submit = document.getElementById('submit-voucher');
const vouchers = document.getElementById('vouchers');
console.log(vouchers);
// open add voucher page
add_voucher_btn.onclick = () => {
    add_voucher_page.style.display = 'inline';
};

function addVoucherItem(data, id) {
    vouchers.appendChild(createItem(data, id, addDeleteVoucherBtn));
}

function addDeleteVoucherBtn(item, id) {
    let btn = document.createElement('button');
    btn.innerHTML = 'Delete';
    btn.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/eatery/profile/remove_voucher', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ token: token, id: id }));
        if (!this.response) {
            vouchers.removeChild(item);
        } else {
            alert('delete failed');
        }
    }
    item.appendChild(btn);
}

function loadVouchers() {
    console.log('here')
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/get_voucher', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const data of JSON.parse(this.response)['vouchers']) {
                addVoucherItem(data, data['id']);
            }
        }
    }
    xhr.send(`{ "token":"${token}" }`)
    // add data to schedule list
}

loadVouchers();



// close subpage
document.onmousedown = (e) => {
    if (getCurrPage() === 'view-voucher') {
        if ((!add_voucher_page.contains(e.target)) && 
            add_voucher_page.style.display === 'inline'&&
            (!add_voucher_page.contains(e.target))) {
            add_voucher_page.style.display = 'none';
        }
    } else if (getCurrPage() === 'view-schedule'){
        if ((!add_schedule_page.contains(e.target)) && 
            add_schedule_page.style.display === 'inline'&&
            (!add_schedule_btn.contains(e.target))) {
            add_schedule_page.style.display = 'none';
        }
    }   
}

// get the current active page
function getCurrPage() {
    for (const p of pages) {
        if (p.style.display === 'block') {return p.id;}
    }
}
