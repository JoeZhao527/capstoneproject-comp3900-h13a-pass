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
const cuisine_ul = document.getElementById('cuisine-list');

let locationList = {}
let cuisineList = []

function loadDateList() {
    let date_list = generateDateList();
    date_ul.innerHTML = ''

    // all date selection
    let li = document.createElement('li');
    li.innerHTML = 'All dates'
    li.onclick = () => {
        let date_input = document.getElementById('date-input');
        date_input.innerHTML = 'All dates'
        date_input.title = ""
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
        let time_input = document.getElementById('time-input');
        time_input.innerHTML = 'All time'
        time_input.title = ""
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
        }
        time_ul.appendChild(li)
    }
}

function loadCityList() {
    let cityList = generateCityList();
    city_ul.innerHTML = ''

    for (const c of cityList) {
        let li = document.createElement('li');
        li.innerHTML = c;
        li.onclick = () => {
            let city_input = document.getElementById('city-input');
            city_input.innerHTML = c;
            city_input.title = c;
            loadSuburbList(c);
        }
        city_ul.appendChild(li)
    }

    // load default value for city
    let city_input = document.getElementById('city-input');
    let city = city_ul.firstChild.innerHTML;
    city_input.innerHTML = city;
    city_input.title = city;
    loadSuburbList(city);
}

function loadSuburbList(city) {
    let suburbList = locationList[city];
    suburb_ul.innerHTML = ''

    let li = document.createElement('li');
    li.innerHTML = 'All suburb'
    li.onclick = () => {
        let suburb_input = document.getElementById('suburb-input');
        suburb_input.innerHTML = 'All suburb'
        suburb_input.title = ""
    }
    suburb_ul.appendChild(li)

    // 24 hours 00/30 minutes selection
    for (const s of suburbList) {
        let li = document.createElement('li');
        li.innerHTML = s;
        li.onclick = () => {
            let suburb_input = document.getElementById('suburb-input');
            suburb_input.innerHTML = s;
            suburb_input.title = s;
        }
        suburb_ul.appendChild(li)
    }
}

function loadCuisineList() {
    cuisine_ul.innerHTML = ''

    let li = document.createElement('li');
    li.innerHTML = 'All cuisines'
    li.onclick = () => {
        let input = document.getElementById('cuisine-input');
        input.innerHTML = 'All cuisines'
        input.title = ""
    }
    cuisine_ul.appendChild(li)

    // 24 hours 00/30 minutes selection
    for (const item of cuisineList) {
        let li = document.createElement('li');
        li.innerHTML = item;
        li.onclick = () => {
            let input = document.getElementById('cuisine-input');
            input.innerHTML = item;
            input.title = item;
        }
        cuisine_ul.appendChild(li)
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
        let item = { date:`${yyyy}-${mm}-${dd}`, display:`${day}  ${dd}th ${monthMap(mm)}`}
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

// get city dictionary, stores it in locationList
function generateCityList() {
    let cityList = []
    for (var city in locationList) {
        cityList.push(city);
    }
    return cityList;
}

// get location list from server
function getLocationList() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/diner/home/get_location', false);
    xhr.send()
    res = JSON.parse(xhr.response)
    locationList = res;
    return res
}

// get cuisine list from server
function getCuisineList() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/diner/home/get_cuisine', false);
    xhr.send()
    res = JSON.parse(xhr.response)['cuisine']
    cuisineList = res;
    return res;
}

loadDateList();
loadTimeList();

getLocationList(); // get location from server
generateCityList();
loadCityList();

getCuisineList(); // get cuisines from server
loadCuisineList();

/* submit filter and apply search */
const submit_filter = document.getElementById('filter-submit');
let input_list = document.getElementById('filter').getElementsByTagName('span');
const eatery_section = document.getElementById('eateries');

submit_filter.onclick = () => {
    getFilterAndLoad();
}

function getFilterAndLoad() {
    let filter_data = {}
    for (const i of input_list) {
        if (i.id == '') break;
        let k = i.id.split('-')[0]
        filter_data[k] = i.title;
    }

    // create filter data location attr
    filter_data['location'] = filter_data['city']+','+filter_data['suburb'];
    
    searchEateryByFilter(filter_data);
}

function searchEateryByFilter(filter_data) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/get_eatery', true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                let res = JSON.parse(this.response)['eateries']
                loadEateries(res)
            } else {
                alert('filter search failed')
            }
        }
    }
    xhr.send(JSON.stringify(filter_data))
}

/**
 * Load the eateries into the main page
 * @param {Array} eateries a list of eateries, with eatery name, location, images etc.
 */
function loadEateries(eateries) {
    eatery_section.innerHTML = ''
    let default_img_src = '../static/images/food_1.jpg';

    for (let idx = 0; idx < eateries.length; idx++) {
        // address image icon 
        let addr_img = new Image();
        addr_img.src = '../static/images/city.png';
        addr_img.className = 'icon child';

        // cuisine image icon
        let cuisine_img = new Image();
        cuisine_img.src = '../static/images/cuisine.png';
        cuisine_img.className = 'icon child';

        let eatery = eateries[idx];
        let img_src = eatery['eatery_image']
        let name = eatery['eatery_name']
        let addr = eatery['city'] + ', ' + eatery['suburb']
        let cuisine = eatery['cuisine']
        let eatery_path = `/eatery/profile/${eatery['id']}`;
        let container = document.createElement('div');
        let sub_container = document.createElement('div');
        let img_div = document.createElement('div');
        let name_div = document.createElement('div');
        let h1 = document.createElement('h1');

        // make eatery name element
        h1.innerHTML = name;
        name_div.appendChild(h1);

        let content_divs = []
        for (let i = 0; i < 3; i++) {
            let div = document.createElement('div');
            div.className = 'content';
            content_divs.push(div)
        }

        let eatery_img = new Image();
        if (img_src !== '') eatery_img.src = img_src;
        else eatery_img.src = default_img_src;
        img_div.appendChild(eatery_img);

        // address span
        let addr_span = document.createElement('span');
        addr_span.className = 'child'
        addr_span.innerHTML = addr;

        // make address line
        content_divs[0].appendChild(addr_img);
        content_divs[0].appendChild(addr_span);


        // cuisine span
        let cuisine_span = document.createElement('span');
        cuisine_span.className = 'child';
        cuisine_span.innerHTML = cuisine;

        content_divs[1].appendChild(cuisine_img);
        content_divs[1].appendChild(cuisine_span);


        // rating span, currently static
        let star_div = document.createElement('div')
        star_div.className = 'Stars'
        star_div.style = '--rating: 4.3';
        star_div.innerHTML = ' 4.3 ';

        content_divs[2].appendChild(star_div);

        // append name, address, cusine and stars to sub_container
        sub_container.appendChild(name_div);
        for (const d of content_divs) {
            console.log(typeof d)
            sub_container.appendChild(d);
        }

        container.appendChild(img_div);
        container.appendChild(sub_container);

        container.onclick = () => {
            window.location.href = eatery_path;
        }

        console.log(container)

        eatery_section.appendChild(container);
    }
    /*
    <div>
        <div>
            <img src="../static/images/food_1.jpg" alt="">
        </div>
        <div>
            <div>
                <h1>eatery name</h1>
            </div>
            <div class="content">
                <img class="icon child" src="../static/images/city.png" alt="">
                <span class="child">Sydney, Kensington</span>
            </div>
            <div class="content">
                <img class="icon child" src="../static/images/cuisine.png" alt="">
                <span class="child">cuisine</span>
            </div>
            <div class="content">
                <div class="Stars" style="--rating: 3.3;"> 3.3 </div>
            </div>
        </div>
    </div>
    */

}

getFilterAndLoad();