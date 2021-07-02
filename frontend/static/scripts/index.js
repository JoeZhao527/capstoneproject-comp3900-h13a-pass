// path
const eatery_home = '/'

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
const logout = document.getElementById('logout');

logout.onclick = () => {
    sessionStorage.removeItem('token');
    window.location.href = eatery_home;
}

/* content */
let token = sessionStorage.getItem('token');

// profile
const profile_form = document.getElementById('profile-form');
const profile_item = profile_form.getElementsByTagName('input');

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
            console.log(_data);
            loadEateryData(_data);
        }
    }
    xhr.send(`{"token":"${_token}"}`);
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
    console.log(data)
    let token = updateProfile(data);
    if (token !== '') {
        console.log('success')
    } else {
        alert('sign up failed')
    }
}

function updateProfile(data) {
    // send data and receive token
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/eatery_private_profile/update', false);
    xhr.send(JSON.stringify(data))
    console.log('here');
    return xhr.response;
}