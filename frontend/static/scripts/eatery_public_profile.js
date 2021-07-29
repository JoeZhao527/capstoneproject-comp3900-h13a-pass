/* token and id */
let token = sessionStorage.getItem('token');
let user_id = sessionStorage.getItem('id');
let utype = sessionStorage.getItem('utype');
let profile_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
console.log(user_id)
/* path */
const eatery_home = '/eatery/home';
const diner_home = '/diner/home';
const eatery_private = '/eatery/profile/private';
const diner_register = '/diner/register';

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
    if (utype === 'diner') window.location.href = '/diner/profile/private';
    else window.location.href = '/eatery/profile/private';
}

home_btn.onclick = () => {
    window.location.href = diner_home;
}

sign_up_btn.onclick = () => {
    window.location.href = diner_register;
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
const menu_section = document.getElementById('menu-section');

/**
 * @param {*} eatery_id 
 * get eatery information from backend by its id,
 * then load the data to web page
 */
function getInformation(eatery_id) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/eatery/profile/${eatery_id}/get_info`, true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let data = JSON.parse(this.response)
            // load description section
            load_description(data['description'], data['cuisine'], data['menu']);
            // load contact section
            load_contact(data);
            // load header
            load_header(data['eatery_name']);
            /**
             * getAddress is a function is 'google_map.js', which is used to get latitude and longitude by an address,
             * and load the google map
             */
            getAddress(addr)
        }
    }
    xhr.send();
}

// load description and cuisine to web page
function load_description(_description, _cuisine, menu_src) {
    cuisines.innerHTML = _cuisine;
    description.innerHTML = '';
    let p = document.createElement('p');
    p.innerHTML = _description;

    let iframe;
    if (menu_src) {
        iframe = document.createElement('iframe');
        iframe.src = menu_src;
    } else {
        iframe = document.createElement('h1');
        iframe.innerHTML = "No menu available for this eatery";
    }
    
    let menu_link = document.createElement('a');
    menu_link.innerHTML = 'view menu';
    menu_link.className = 'menu-link';
    menu_link.onclick = () => {
        menu_section.innerHTML = ''
        menu_section.appendChild(iframe)
        menu_section.style.display = 'inline';
    }
    description.appendChild(p)
    description.appendChild(menu_link)
}

// load contact item to web page
function load_contact(data) {
    // contact_item is a list of attribute name:
    // ['address', 'phone', 'email', 'city', 'suburb']
    for (const item of contact_item) {
        let p = item.getElementsByTagName('p')[0];
        addr[p.id] = data[p.id];
        p.innerHTML = data[p.id];
    }
}

// load header, with eatery's name
function load_header(_eatery_name) {
    eatery_name.innerHTML = _eatery_name;
}

let addr = {}
// load the whole information section on loading the page
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
    // get the minimum date for the filter, which is today
    var minDay = new Date();
    var dd = String(minDay.getDate()).padStart(2, '0');
    var mm = String(minDay.getMonth() + 1).padStart(2, '0');
    var yyyy = minDay.getFullYear();
    minDay = yyyy + '-' + mm + '-' + dd;
    
    // get the maximum date for the filter, which is 7 days later
    var maxDay = new Date();
    maxDay.setDate(maxDay.getDate() + 7); 
    var dd = String(maxDay.getDate()).padStart(2, '0');
    var mm = String(maxDay.getMonth() + 1).padStart(2, '0');
    var yyyy = maxDay.getFullYear();
    maxDay = yyyy + '-' + mm + '-' + dd;
    
    // set the voucher filter and header for the voucher booking section
    book_section.innerHTML = `<h2> Book A Voucher!</h2> 
    <label>select date:</lable>
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
    public_loadVouchers(profile_id);
}

let voucher_list = []

/**
 * 
 * @param {object} item contains:
 *      1. 'data': voucher's date, start time, end time, discount, and number of vouchers etc.
 *      2. 'group_id': voucher's group id. group id can be used to book/cancel voucher by diner,
 *          or delete/add voucher by eatery
 * addVoucherItem will be called by 'public_loadVouchers' in load_vouchers.js, it uses the date
 * in date_filter, display all the vouchers can be booked at that date
 * 
 */
function addVoucherItem(data) {
    let group_id = data['group_id']
    let amount = data['amount']
    // date_filter contains the date to display voucher, 
    if (data['date'] == date_filter) {
        let date = stringifyDate(data['date'], data['weekday']);
        let period = stringifyTime(data['start_time'], data['end_time']);
        let discount = stringifyDiscount(data['discount']);
        let num = stringifyNum(amount);
    
        // create node
        /**
         * Voucher structure:
            <div class="voucherNode">
                <div class="discountNode"></div>
                <div class="voucherTimeNode">
                    <div class="dateNode"></div>
                    <div class="timeNode"></div>
                    <div class="numNode"></div>
                </div>
                <div class="bookNode"></div>
            </div>
         * this will be a voucher node, append to the voucher container
         */
        let voucherNode = document.createElement('div');    // the voucher information container
    
        let dateNode = document.createElement('div');       // voucher's date div
        dateNode.innerHTML = date;
        let periodNode = document.createElement('div');     // voucher's start time, end time div
        periodNode.innerHTML = date + '  ' + period;
        let discountNode = document.createElement('div');   // voucher's discount div
        discountNode.innerHTML = discount;
        discountNode.className = 'discount';
        let numNode = document.createElement('h3');          // voucher's number left div
        numNode.innerHTML = num;
        let bookNode = document.createElement('div');       // book voucher button div
        bookNode.innerHTML = "book";
        bookNode.className = "book";
    
        let voucherTimeNode = document.createElement('section'); // div contains voucher date and time
        voucherTimeNode.appendChild(periodNode);
        voucherTimeNode.appendChild(numNode);
    
        voucherNode.appendChild(discountNode);
        voucherNode.appendChild(voucherTimeNode);
        voucherNode.appendChild(bookNode);

        voucherNode.onclick = () => {
            /**
             * function from book_voucher.js
             * @param utype: user type, "diner" or "eatery"
             * @param group_id: voucher's group id, can be used by diner to book voucher
             */
            checkUser(utype, group_id);
        }

        voucher_container.appendChild(voucherNode);
        
        // voucher section will have a no-voucher today onload
        // if a voucher is added, remove the "no voucher" text
        let no_res = voucher_container.getElementsByTagName('p')[0]
        if (typeof no_res !== 'undefined') voucher_container.removeChild(no_res);
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
 * @param {string} start start time of voucher
 * @param {string} end  end time of voucher
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

/* get comments for this eatery */
const comment_container = document.getElementById('comment-container')
const review_filter = document.getElementById('review-filter')

review_filter.onchange = () => {
    getReviews()
}

// get reviews, avg rating and number of reviews from backend
function getReviews() {
    let sort_order = review_filter.value
    console.log(sort_order)
    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/eatery/profile/${profile_id}/get_reviews`, true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                let res = JSON.parse(this.response)
                let reviews = res['reviews']
                let num_reviews = res['review_number']
                let avg_rating = res['avg_rating']
                loadReviews(reviews, num_reviews, avg_rating);
            } else {
                alert('get comment failed')
            }
        }
    }
    xhr.send(JSON.stringify({ sort:sort_order }))
}

const stars = document.getElementsByClassName('Stars')[0];
const number_of_reviews  = document.getElementById('num-reviews');

function loadReviews(reviews, num, avg_rating) {
    comment_container.innerHTML = ''
    stars.style = `--rating: ${avg_rating}`;
    number_of_reviews.innerHTML = `${num} reviews`;

    for (const rev of reviews) {
        let div = document.createElement('div');
        let h4 = document.createElement('h4');
        let p = document.createElement('p');
        let hr = document.createElement('hr')
        let starDiv = document.createElement('div');
        starDiv.className = 'Stars';
        starDiv.style = `--rating: ${rev['rating']}`;

        h4.innerHTML = `${rev['diner_name']} \xa0\xa0\xa0`
        h4.appendChild(starDiv)
        p.innerHTML = rev['comment']

        div.appendChild(h4);
        div.appendChild(p);
        div.appendChild(hr);

        comment_container.appendChild(div)
    }
}

getReviews();