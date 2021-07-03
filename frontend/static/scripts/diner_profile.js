
/* main and nav bar*/
const main = document.getElementById('main');
const nav_bar = document.getElementById('nav-bar');

// debug line
console.log(sessionStorage.getItem('token'));

/* eatery profile info */
const info_item = document.getElementById('eatery-info').getElementsByTagName('li');

// get eatery's info by its token
function getEateryData() {
    let _token = sessionStorage.getItem('token');
    let _data = {}
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery_private_profile/info', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            for (const [key, value] of Object.entries(JSON.parse(this.response))) {
                _data[key] = value;
            }
            dirty_fix_data(_data)
            loadEateryData(_data);
        }
    }
    xhr.send(`{"token":"${_token}"}`);
}

function dirty_fix_data(_data) {
    _data['fname'] = _data['first_name']
    _data['lname'] = _data['last_name']
    _data['ename'] = _data['eatery_name']
}

// load eatery data to profile
function loadEateryData(_data) {
    Array.from(info_item).forEach(e => {
        if (_data[e.id] !== 'undefined') {
            e.innerHTML = e.innerHTML+'\xa0\xa0\xa0\xa0\xa0'+_data[e.id]
        }
    });
}

getEateryData();

/* buttons */
// diner home page
const home_btn = document.getElementById('home');
home_btn.addEventListener('click', function() {
    alert('diner home page not implmented yet');
});

// logout
const logout_btn = document.getElementById('logout');
logout_btn.addEventListener('click', function() {
    if (logout()) {
        sessionStorage.removeItem('token');
        window.location.href = eatery_home;
    } else {
        alert('logout failed for unknown reasons')
    }
})

/**
 * send logout request to backend
 */
 function logout() {
    let token = window.sessionStorage.getItem('token');
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/logout', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(`{"token":"${token}"}`);
    console.log(xhr.response);
    return xhr.response
}

// back eatery home
const back_btn = document.getElementById('back');
back_btn.onclick = () => {
    window.location.href = eatery_home;
}
