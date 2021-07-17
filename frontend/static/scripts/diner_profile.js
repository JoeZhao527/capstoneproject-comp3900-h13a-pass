// path
const eatery_home = '/'
const diner_home = '/diner/home';

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

// get diner's info by its token
function getDinerData() {
    let _data = {}
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/profile/private/info', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const [key, value] of Object.entries(JSON.parse(this.response))) {
                _data[key] = value;
            }
            console.log(_data);
            loadDinerData(_data);
        }
    }
    xhr.send(`{"token":"${token}"}`);
}
getDinerData();

// load diner data to profile
function loadDinerData(data) {
    Array.from(profile_item).forEach(e => {
        if (e.name) {
            e.value = data[e.name]
        }
    });
}


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
    data['token'] = token;
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
    xhr.open('PUT', '/diner_private_profile/update', false);
    xhr.send(JSON.stringify(data))
    console.log(xhr.response)
    return xhr.response;
}

function mapWeekday(n) {
    const weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return weekday[n]
}


function addDeleteActiveBtn(item, id) {
    let btn = document.createElement('button');
    btn.innerHTML = 'Delete';
    btn.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/diner/profile/remove_active', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ token: token, id: id }));
        if (!this.response) {
            active.removeChild(item);
        } else {
            alert('delete failed');
        }
    }
    item.appendChild(btn);
}

function addActiveItem(data, id) {
    schedules.appendChild(createItem(data,id,addDeleteActiveBtn));
}

function loadActive() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/profile/get_active', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const data of JSON.parse(this.response)['active']) {
                addActiveItem(data, data['id']);
            }
        }
    }
    xhr.send(`{ "token":"${token}" }`)
    // add data to schedule list
}

loadActive();



function addPreviousItem(data, id) {
    Previouss.appendChild(createItem(data, id, addDeletePreviousBtn));
}

function addDeletePreviousBtn(item, id) {
    let btn = document.createElement('button');
    btn.innerHTML = 'Delete';
    btn.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/diner/profile/remove_previous', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ token: token, id: id }));
        if (!this.response) {
            Previouss.removeChild(item);
        } else {
            alert('delete failed');
        }
    }
    item.appendChild(btn);
}

function loadPrevious() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/profile/get_previous', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const data of JSON.parse(this.response)['Previouss']) {
                addPreviousItem(data, data['id']);
            }
        }
    }
    xhr.send(`{ "token":"${token}" }`)
}

loadPrevious();



// get the current active page
function getCurrPage() {
    for (const p of pages) {
        if (p.style.display === 'block') {return p.id;}
    }
}
