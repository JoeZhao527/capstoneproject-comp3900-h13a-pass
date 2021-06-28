// paths
const eatery_home = '/';

/* main and nav bar*/
const main = document.getElementById('main');
const nav_bar = document.getElementById('nav-bar');

// debug line
console.log(sessionStorage.getItem('token'));

/* eatery profile info */
const info_item = document.getElementById('eatery-info').getElementsByTagName('li');

// get eatery's info by its token
function getEateryData() {
    let token = sessionStorage.getItem('token');
    let _data = {
        fname: 'joe',
        lname: 'zhao',
        ename: 'eatery_name',
        email: '1016859319@qq.com',
        phone: '0452568128',
        address: 'address, 2052 UNSW',
    }
    return _data
}

// load eatery data to profile
function loadEateryData(_data) {
    Array.from(info_item).forEach(e => {
        e.innerHTML = e.innerHTML+'\xa0\xa0\xa0\xa0\xa0'+_data[e.id]
    });
}

let data = getEateryData();
loadEateryData(data);

/* buttons */
// diner home page
const home_btn = document.getElementById('home');
home_btn.addEventListener('click', function() {
    alert('diner home page not implmented yet');
});

// logout
const logout_btn = document.getElementById('logout');
logout_btn.addEventListener('click', function() {
    sessionStorage.removeItem('token');
    window.location.href = eatery_home;
})

// back eatery home
const back_btn = document.getElementById('back');
back_btn.onclick = () => {
    window.location.href = eatery_home;
}

/* subpage operations */
// close subpage
function closeSubpage(page) {
    page.style.display = 'none';
    main.style.display = 'inline';
    nav_bar.style.display = 'inline';
}

// open subpage
function openSubpage(page) {
    page.style.display = 'inline';
    main.style.display = 'none';
    nav_bar.style.display = 'none';
}

/* edit profile */
const edit_btn = document.getElementById('edit-profile');
const edit_page = document.getElementById('edit-page');
const close_edit = edit_page.getElementsByClassName('close')[0];

edit_btn.onclick = () => {
    openSubpage(edit_page)
};

close_edit.onclick = () => {
    closeSubpage(edit_page);
}

/* select add type */
const turn_schedule_btn = document.getElementById('schedule-btn');
const turn_voucher_btn = document.getElementById('voucher-btn');
const schedule = document.getElementById('by-schedule');
const voucher = document.getElementById('by-voucher');

function displayScheduleList() {
    turn_schedule_btn.style.setProperty('border-bottom', 'white 4px solid');
    turn_voucher_btn.style.setProperty('border-bottom', 'none');
    schedule.style.display = 'inline';
    voucher.style.display = 'none';
}

function displayVoucherList() {
    turn_voucher_btn.style.setProperty('border-bottom', 'white 4px solid');
    turn_schedule_btn.style.setProperty('border-bottom', 'none');
    schedule.style.display = 'none';
    voucher.style.display = 'inline';
}

turn_schedule_btn.onclick = () => {
    displayScheduleList();
}

turn_voucher_btn.onclick = () => {
    displayVoucherList();
}

displayScheduleList();

/* add schedule */
const add_schedule_btn = document.getElementById('add-schedule-btn');   // add schedule button in main
const add_schedule_page = document.getElementById('add-schedule');      // subpage container
const close_schedule = document.getElementsByClassName('close')[1];     // close button in subpage
const schedule_form = document.getElementById('schedule-form');         // form in subpage
const schedule_elem = schedule_form.elements;                           // form elements
const schedule_submit = document.getElementById('submit-schedule');     // submit button in subpage

let schedule_data = {}

// open and close schedule page
add_schedule_btn.onclick = () => {
    openSubpage(add_schedule_page);
};

close_schedule.onclick = () => {
    schedule_form.reset();
    closeSubpage(add_schedule_page);
}

// submit form listener, store data
schedule_form.onsubmit = (e) => {
    e.preventDefault();
    Array.from(schedule_elem).forEach(function(e) {
        if (e.type !== 'submit') {
            schedule_data[e.id] = e.value;
        }
    })
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/add_schedule', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(schedule_data));

    if (xhr.response) {
        addScheduleItem(xhr.response);
    }

    schedule_form.reset();
    closeSubpage(add_schedule_page);
    schedule_data = {}
}

// add item into schedule list
const schedule_ul = document.getElementById('schedule');

function addScheduleItem(id) {
    let schedule_item = document.createElement('ul');
    // add data to schedule
    for (const [key, value] of Object.entries(schedule_data)) {
        console.log(key, value, typeof value);
        let schedule_li = document.createElement('li');
        schedule_li.appendChild(document.createTextNode(value));
        schedule_item.appendChild(schedule_li);
    }
    // add delete button to schedule
    
    addEditBtn(schedule_item, id);
    addDeleteBtn(schedule_item, id);
    schedule_ul.appendChild(schedule_item);
}

/**
 * @param item parent of li
 * add the li with a button delete button inside to item
 */
function addDeleteBtn(item, _id) {
    let btn = document.createElement('button');
    btn.innerHTML = 'Delete';
    btn.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/eatery/profile/remove_schedule', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ id: _id }));
        if (xhr.response === 'true') {
            schedule_ul.removeChild(item);
        } else {
            alert('delete failed');
        }
    }
    item.appendChild(btn);
}

/**
 * @param item parent of li
 * add the li with a edit button to item
 */
function addEditBtn(item, id) {
    let btn = document.createElement('button');
    btn.innerHTML = 'Edit';
    btn.onclick = () => {
        console.log("edit clicked");
    }
    btn.onmouseover = () => {
        btn.style.backgroundColor = 'lightskyblue';
    }
    btn.onmouseleave = () => {
        btn.style.backgroundColor = 'white';
    }
    item.appendChild(btn);
}