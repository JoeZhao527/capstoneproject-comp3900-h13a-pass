// paths
const diner_register = '/diner/register';
const diner_private_profile = '/diner/private_profile';
const diner_home = '/diner/home';
const eatery_home = '/eatery/home';

// user's identifiers
let token = sessionStorage.getItem('token');
let user_id = sessionStorage.getItem('id');
let utype = sessionStorage.getItem('utype');

console.log(token, user_id, utype)

// buttons in nav bar
const for_eatery_btn = document.getElementById('for-eatery-btn');
const sign_up_btn = document.getElementById('sign-up-btn');
const login_btn = document.getElementById('login-btn');
const logout_btn = document.getElementById('logout-btn');
const profile_btn = document.getElementById('profile-btn');

const logged_in_btns = [logout_btn, profile_btn];
const logged_out_btns = [login_btn, sign_up_btn];

function loadPage() {
    token = sessionStorage.getItem('token');
    if (token === 'undefined' || token === null) display_default();
    else display_user();
}
function display_default() {
    for (const btn of logged_in_btns) btn.style.display = 'none';
    for (const btn of logged_out_btns) btn.style.display = 'inline';
}

function display_user() {
    for (const btn of logged_in_btns) btn.style.display = 'inline';
    for (const btn of logged_out_btns) btn.style.display = 'none';
}

loadPage();

// switching pages
for_eatery_btn.onclick = () => { window.location.href = eatery_home }

sign_up_btn.onclick = () => { window.location.href = diner_register }

profile_btn.onclick = () => { window.location.href = diner_private_profile }

// filter logic
const filter_inputs = document.getElementsByClassName('filter-input')
const filter_inputs_ul = document.getElementById('filter').getElementsByTagName('ul');

// display corresponding selection field when click a filter input
for (let i = 0; i < filter_inputs.length; i++) {
    filter_inputs[i].onclick = () => {
        for (let j = 0; j < filter_inputs_ul.length; j++) {
            if (i == j) {
                if (filter_inputs_ul[j].style.display == 'block') filter_inputs_ul[j].style.display = 'none';
                else filter_inputs_ul[j].style.display = 'block';
            } else {
                filter_inputs_ul[j].style.display = 'none'
            }
        }
    }
}

// hide the ul when click on outside of the ul
document.onmouseup = (e) => {
    for (let i = 0; i < filter_inputs_ul.length; i++) {
        let ul = filter_inputs_ul[i];
        let input = filter_inputs[i];
        if (ul.style.display == 'block' && !ul.contains(e.target) && !input.contains(e.target)) {
            ul.style.display = 'none'
        }
    }
}

/* filter load selection list */
const date_ul = document.getElementById('date-list');
const time_ul = document.getElementById('time-list');
const city_ul = document.getElementById('city-list');
const suburb_ul = document.getElementById('suburb-list');


function loadDateList() {
    let date_list = generateDateList();
    date_ul.innerHTML = ''

    // all date selection
    let li = document.createElement('li');
    li.innerHTML = 'All dates'
    li.onclick = () => {
        let date_input = document.getElementById('date-input');
        date_input.innerHTML = 'All dates'
        date_input.title = 'All dates'
    }
    date_ul.appendChild(li)

    // next 7 days selection
    for (const date of date_list) {
        let li = document.createElement('li');
        li.innerHTML = date['display']
        li.onclick = () => {
            let date_input = document.getElementById('date-input');
            date_input.innerHTML = date['display']
            date_input.title = date['date']
            console.log(date_input)
        }
        date_ul.appendChild(li)
    }
}

function loadTimeList() {
    let timeList = generateTimeList();
    time_ul.innerHTML = ''

    // all date selection
    let li = document.createElement('li');
    li.innerHTML = 'All time'
    li.onclick = () => {
        let date_input = document.getElementById('time-input');
        date_input.innerHTML = 'All time'
        date_input.title = 'All time'
    }
    time_ul.appendChild(li)

    // 24 hours 00/30 minutes selection
    for (const t of timeList) {
        let li = document.createElement('li');
        li.innerHTML = t;
        li.onclick = () => {
            let time_input = document.getElementById('time-input');
            time_input.innerHTML = t;
            time_input.title = t;
            console.log(time_input)
        }
        time_ul.appendChild(li)
    }
}

// generate next 7 days 
function generateDateList() {
    let date_list = []
    let today = new Date();
    for (let i = 0; i < 7; i++) {
        // make a date 
        let dd = String(today.getDate()).padStart(2, '0'); // date
        let mm = String(today.getMonth() + 1).padStart(2, '0');  // Month
        let day = weekdayMap(today.getDay()); // weekday
        let yyyy = today.getFullYear()
        let item = { date:`${dd}/${mm}/${yyyy}`, display:`${day}  ${dd}th ${monthMap(mm)}`}
        date_list.push(item);

        today.setDate(today.getDate() + 1);
    }
    return date_list;
}

// map a string like '01' to month
function monthMap(mon) {
    let month = ['Dec', 'Jun', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
    return month[parseInt(mon)]
}

// map an integer like 3 to week
function weekdayMap(w) {
    let week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    return week[w]
}

// generate times
function generateTimeList() {
    let timeList = []
    for (let i = 0; i < 24; i++) {
        let h = String(i).padStart(2, '0');
        timeList.push(`${h}:00`)
        timeList.push(`${h}:30`)
    }
    return timeList;
}

function generateCityList() {
    
}

loadDateList();
loadTimeList();