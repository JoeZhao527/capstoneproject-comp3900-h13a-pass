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
const sign_up_btn = document.getElementById('sign-up-btn');
const profile_btn = document.getElementById('profile-btn');

const user_btns = [logout_btn, profile_btn];
const default_btns = [login_btn, sign_up_btn];

/* nav bar display logic */
function loadPage() {
    token = sessionStorage.getItem('token');
    user_id = sessionStorage.getItem('id');
    utype = sessionStorage.getItem('utype');
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
const google_map = document.getElementById('google-map')    // google map page

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
            load_description(data['description'], data['cuisine']);
            load_contact(data);
            load_header(data['eatery_name']);
            getAddress(addr)
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
        addr[p.id] = data[p.id];
        p.innerHTML = data[p.id];
    }
}

function load_header(_eatery_name) {
    eatery_name.innerHTML = _eatery_name;
}

// will be used in map
let addr = {}

getInformation(profile_id);


/* switching between description and contact */
// description button and contact button
const description_btn = document.getElementById('description-btn');
const contact_btn = document.getElementById('contact-btn');
const map_btn = document.getElementById('map-btn');

const content_pages = [description, contact, google_map];
description_btn.onclick = () => {
    displayContent(description);
}

contact_btn.onclick = () => {
    displayContent(contact);
}

map_btn.onclick = () => {
    displayContent(google_map);
}

function displayContent(page) {
    for (const p of content_pages) {
        if (p === page) p.style.display = 'block';
        else p.style.display = 'none';
    }
}

displayContent(description);

/* voucher booking */
const book_section = document.getElementById('book-section');

/**
 * add a date fileter to the booking section
 */
function loadVoucherFilter() {
    var minDay = new Date();
    var dd = String(minDay.getDate()).padStart(2, '0');
    var mm = String(minDay.getMonth() + 1).padStart(2, '0');
    var yyyy = minDay.getFullYear();
    minDay = yyyy + '-' + mm + '-' + dd;
    
    var maxDay = new Date();
    maxDay.setDate(maxDay.getDate() + 7); 
    var dd = String(maxDay.getDate()).padStart(2, '0');
    var mm = String(maxDay.getMonth() + 1).padStart(2, '0');
    var yyyy = maxDay.getFullYear();
    maxDay = yyyy + '-' + mm + '-' + dd;
    
    book_section.innerHTML = `<h2> Book A Voucher!</h2> select date:
    <input id="date-filter" type="date" min="${minDay}" max="${maxDay}" value="${minDay}">
    <div id="voucher-container"><p>No Vouchers Avaliable Today</p></div>`;
}

// add date filter to booking section when page load
loadVoucherFilter();

const voucher_container = document.getElementById('voucher-container');

// get date fileter
const date_filter_input = document.getElementById('date-filter');
let date_filter = date_filter_input.value;

date_filter_input.onchange = (e) => {
    date_filter = e.target.value;
    voucher_container.innerHTML = '<p>No Vouchers Avaliable Today</p>';
    public_loadVouchers(profile_id);
}

let voucher_list = []

function addVoucherItem(item) {
    let data = item['data']
    let ids = item['id']
    if (data['date'] == date_filter) {
        let date = stringifyDate(data['date'], data['weekday']);
        let period = stringifyTime(data['start_time'], data['end_time']);
        let discount = stringifyDiscount(data['discount']);
        let num = stringifyNum(ids.length);
    
        // create node
        /**
         * Voucher structure:
            <div class="voucherNode">
                <div class="discountNode"></div>
                <div class="voucherTimeNode">
                    <div class="dateNode"></div>
                    <div class="timeNode"></div>
                </div>
                <div class="bookNode"></div>
            </div>
         */
        let voucherNode = document.createElement('div');
    
        let dateNode = document.createElement('div');
        dateNode.innerHTML = date;
        let periodNode = document.createElement('div');
        periodNode.innerHTML = period;
        let discountNode = document.createElement('div');
        discountNode.innerHTML = discount; // discount "10% OFF"
        discountNode.className = 'discount';
        let numNode = document.createElement('p');
        numNode.innerHTML = num;
        let bookNode = document.createElement('div');
        bookNode.innerHTML = "book";
        bookNode.className = "book";
    
        let voucherTimeNode = document.createElement('section');
        voucherTimeNode.appendChild(dateNode);
        voucherTimeNode.appendChild(periodNode);
        voucherTimeNode.appendChild(numNode);
    
        voucherNode.appendChild(discountNode);
        voucherNode.appendChild(voucherTimeNode);
        voucherNode.appendChild(bookNode);

        voucherNode.onclick = () => {
            checkUser(utype, ids);
        }

        voucher_container.appendChild(voucherNode);

        // if a voucher is added, remove the "no voucher" text
        let no_res = voucher_container.getElementsByTagName('p')[0]
        voucher_container.removeChild(no_res);
    }
}

/**
 * 
 * @param date date of the voucher
 * @param weekday weekday of the voucher
 * @returns a date + weekday string, e.g. 07-21 Tue
 */
function stringifyDate(date, weekday) {
    return date.split('-')[1] + '-' + date.split('-')[2] + ' ' + weekday;
}

/**
 * 
 * @param {string} start 
 * @param {string} end 
 * @returns valid time for voucher, e.g. 16:00 - 20:00
 */
function stringifyTime(start, end) {
    return start + ' ~ ' + end;
}

function stringifyDiscount(discount) {
    return `${discount}%\n OFF!`
}

function stringifyNum(len) {
    return `Only ${len} Vouchers Left!`;
}