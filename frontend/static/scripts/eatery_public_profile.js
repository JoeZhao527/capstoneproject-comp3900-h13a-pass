/* token and id */
let token = sessionStorage.getItem('token');
let user_id = sessionStorage.getItem('id');
let utype = sessionStorage.getItem('utype');
let profile_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);

/* path */
const eatery_home = '/eatery/home';
const diner_home = '/diner/home';
const eatery_private = '/eatery/profile/private';

/* buttons */
const home_btn = document.getElementById('home-btn');
const login_btn = document.getElementById('login-btn');
const logout_btn = document.getElementById('logout-btn');
const sign_up_btn = document.getElementById('sign-up-btn')
const profile_btn = document.getElementById('profile-btn');

const user_btns = [logout_btn, profile_btn];
const default_btns = [login_btn, sign_up_btn];

/* nav bar display logic */
function loadPage() {
    token = sessionStorage.getItem('token');
    user_id = sessionStorage.getItem('id');
    utype = sessionStorage.getItem('utype');
    console.log(token)
    console.log(user_btns, default_btns)
    if (token) displayUser();
    else displayDefault();
}

function displayUser() {
    for (const btn of user_btns) {btn.style.display = 'inline-block'}
    for (const btn of default_btns) {btn.style.display = 'none'}
}

function displayDefault() {
    for (const btn of user_btns) {btn.style.display = 'none'}
    for (const btn of default_btns) {btn.style.display = 'inline-block'}
}

loadPage();

/* nav bar jump logic */
profile_btn.onclick = () => {
    if (utype === 'diner') window.location.href = '/diner/profile';
    else window.location.href = '/eatery/profile/private';
}

home_btn.onclick = () => {
    window.location.href = diner_home;
}
/* load image */
const image_section = document.getElementById('image-container');

/* image slide button */
const slide_right = document.getElementById('slide-right');
const slide_left = document.getElementById('slide-left');
let slide_pos = 0;

/* get images by eatery id */
function getImages(eatery_id) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/eatery/profile/${eatery_id}/get_image`, true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let image_list = JSON.parse(this.response)['data']
            for(const item of image_list) {
                let img = new Image();
                img.src = item['image'];
                image_section.appendChild(img);
            }
            // constructing left, right buttons
            let img_list = image_section.getElementsByTagName('img');
            let pos_list = []
            let last_img = img_list[img_list.length-1];
            for (const img of img_list) {
                if (last_img.getBoundingClientRect().right - 
                    img.getBoundingClientRect().left <
                    image_section.clientWidth) {
                        pos_list.push(img.getBoundingClientRect().left)
                        break;
                    }
                pos_list.push(img.getBoundingClientRect().left)
            }
            slide_right.onclick = () => {
                if (slide_pos < pos_list.length-1) { slide_pos = slide_pos + 1; }
                image_section.scroll(pos_list[slide_pos], 0);
            }
            slide_left.onclick = () => {
                if (slide_pos > 0) { slide_pos = slide_pos - 1; }
                image_section.scroll(pos_list[slide_pos], 0);
            }
        }
    }
    xhr.send()
}

getImages(profile_id);

/* load description, contact and other eatery details */
const cuisines = document.getElementById('cuisine');
const description = document.getElementById('description'); // description page
const contact = document.getElementById('contact');         // contact page
const contact_item = contact.getElementsByTagName('div')
const eatery_name = document.getElementById('eatery-name');

// get eatery information by id
function getInformation(eatery_id) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/eatery/profile/${eatery_id}/get_info`, true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let data = JSON.parse(this.response)
            console.log(data)
            load_description(data['description'], data['cuisine']);
            load_contact(data);
            load_header(data['eatery_name']);
        }
    }
    xhr.send();
}

function load_description(_description, _cuisine) {
    cuisines.innerHTML = _cuisine;
    description.innerHTML = _description;
}

function load_contact(data) {
    for (const item of contact_item) {
        let p = item.getElementsByTagName('p')[0];
        console.log(p, p.id)
        p.innerHTML = data[p.id];
    }
}

function load_header(_eatery_name) {
    eatery_name.innerHTML = _eatery_name;
}

getInformation(profile_id);

/* switching between description and contact */
// description button and contact button
const description_btn = document.getElementById('description-btn');
const contact_btn = document.getElementById('contact-btn');
const content_pages = [description, contact];

description_btn.onclick = () => {
    displayContent(description);
}

contact_btn.onclick = () => {
    displayContent(contact);
}

function displayContent(page) {
    for (const p of content_pages) {
        if (p === page) p.style.display = 'block';
        else p.style.display = 'none';
    }
}

displayContent(description);