// path
const eatery_home = '/'
const diner_home = '/diner/home';

// token
let token = sessionStorage.getItem('token');
let id = sessionStorage.getItem('id');

/* side bar swicth page logic */
const side_bar = document.getElementById('side-bar')
const switchs = side_bar.getElementsByTagName('div');
const pages = document.getElementsByClassName('page');

for (let i = 0; i < switchs.length; i++) {
    switchs[i].onclick = () => {
        displayPage(pages[i]);
    }
}
const home_btn = document.querySelector(".home");
home_btn.addEventListener('click', function() {
    window.location.href = diner_home;
})

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


// function addDeleteActiveBtn(item, id) {
//     let btn = document.createElement('button');
//     btn.innerHTML = 'Delete';
//     btn.onclick = () => {
//         let xhr = new XMLHttpRequest();
//         xhr.open('DELETE', '/diner/profile/remove_active', false);
//         xhr.setRequestHeader('Content-Type', 'application/json');
//         xhr.send(JSON.stringify({ token: token, id: id }));
//         if (!this.response) {
//             active.removeChild(item);
//         } else {
//             alert('delete failed');
//         }
//     }
//     item.appendChild(btn);
// }

// function addActiveItem(data, id) {
//     schedules.appendChild(createItem(data,id,addDeleteActiveBtn));
// }

function loadActive() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/profile/get_active', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    const thv = document.getElementById('vouchers')
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            
            // for (const data of JSON.parse(this.response)['active']) {
            //     addActiveItem(data, data['id']);
            // }
            let vlist = JSON.parse(this.response)['vouchers']
            console.log(vlist)
            for(let i = 0; i < vlist.length; i++) {
                let voucher = vlist[i]
                console.log(voucher)
                console.log(voucher['date'])
                let activepart = document.createElement('tr')

                let eaterynode = document.createElement('td')
                let datenode = document.createElement('td')
                let timenode = document.createElement('td')
                let discountnode = document.createElement('td')
                let codenode = document.createElement('td')

                eaterynode.innerHTML = voucher['eatery_name']
                datenode.innerHTML = voucher['date']
                timenode.innerHTML = voucher['start_time']+" - "+voucher['end_time']
                discountnode.innerHTML = voucher['discount']
                codenode.innerHTML = voucher['code']

                activepart.appendChild(eaterynode)
                activepart.appendChild(datenode)
                activepart.appendChild(timenode)
                activepart.appendChild(discountnode)
                activepart.appendChild(codenode)
                addDeleteActiveVoucherBtn(activepart, token, voucher['id']);
                thv.appendChild(activepart)    
            }
        }
    }
    xhr.send(`{"token":"${token}"}`);
    // add data to schedule list
}
loadActive();

function addDeleteActiveVoucherBtn(item,token, id) {
    let deletebtn = document.createElement('button');
    deletebtn.className = 'delete';
    deletebtn.onclick = () => {
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/diner/profile/private/delete_voucher', false);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ token: token, id: id }));
        if (!this.response) {
            vouchers.removeChild(item);
        } else {
            alert('delete failed');
        }
    }
    item.appendChild(deletebtn);
}

function loadPrevious() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/profile/get_previous', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    const thp = document.getElementById('previous')
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            let vlist = JSON.parse(this.response)['vouchers']
            console.log(vlist)
            for(let i = 0; i < vlist.length; i++) {
                let voucher = vlist[i]
                console.log(voucher)
                console.log(voucher['date'])
                let activepart = document.createElement('tr')

                let eaterynode = document.createElement('td')
                let datenode = document.createElement('td')
                let timenode = document.createElement('td')
                let discountnode = document.createElement('td')
                let codenode = document.createElement('td')

                eaterynode.innerHTML = voucher['eatery_name']
                datenode.innerHTML = voucher['date']
                timenode.innerHTML = voucher['start_time']+" - "+voucher['end_time']
                discountnode.innerHTML = voucher['discount']
                codenode.innerHTML = voucher['code']

                activepart.appendChild(eaterynode)
                activepart.appendChild(datenode)
                activepart.appendChild(timenode)
                activepart.appendChild(discountnode)
                activepart.appendChild(codenode)
                addReviewBtn(activepart, voucher['eatery_id']);

                thp.appendChild(activepart)
            }
        }
    }
    xhr.send(`{ "token":"${token}" }`)
}

function loadExpired() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/profile/get_expired', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    const thp = document.getElementById('expired')
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            let vlist = JSON.parse(this.response)['vouchers']
            console.log(vlist)
            for(let i = 0; i < vlist.length; i++) {
                let voucher = vlist[i]
                console.log(voucher)
                console.log(voucher['date'])
                let activepart = document.createElement('tr')

                let eaterynode = document.createElement('td')
                let datenode = document.createElement('td')
                let timenode = document.createElement('td')
                let discountnode = document.createElement('td')
                let codenode = document.createElement('td')

                eaterynode.innerHTML = voucher['eatery_name']
                datenode.innerHTML = voucher['date']
                timenode.innerHTML = voucher['start_time']+" - "+voucher['end_time']
                discountnode.innerHTML = voucher['discount']
                codenode.innerHTML = voucher['code']

                activepart.appendChild(eaterynode)
                activepart.appendChild(datenode)
                activepart.appendChild(timenode)
                activepart.appendChild(discountnode)
                activepart.appendChild(codenode)
                // addReviewBtn(activepart, voucher['eatery_id']);

                thp.appendChild(activepart)
            }
        }
    }
    xhr.send(`{ "token":"${token}" }`)
}
loadExpired()

function addReviewBtn(activepart, eatery_id) {
    let btn = document.createElement('button');
    btn.className = 'review'
    btn.onclick = () => {
        showReviewPage(eatery_id)
    }

    activepart.appendChild(btn)
}

const add_review_btns = document.getElementsByClassName('review');
const review_page = document.getElementById('add-comment-page');
const submit_review = document.getElementById('submit-review');
const comment_input = document.getElementById('comment');
const rating_set = document.getElementById('rating').getElementsByTagName('input');

function showReviewPage(eid) {
    review_page.style.display = 'inline';
    eatery_id = eid;
}

let rating = null;
let comment = null;
let eatery_id = null;

for (const i of rating_set) {
    i.onclick = () => {
        rating = i.value;
    }
}

// when submit button is clicked, get review and comment, submit it
submit_review.onclick = () => {
    comment = comment_input.value
    let msg = document.getElementById('review-msg');
    if (rating == null) {
        msg.innerHTML = 'please select a rating';
        setTimeout(() => {msg.innerHTML = ''}, 2000);
    } else if (comment == null || comment.length == 0) {
        msg.innerHTML = 'please enter a comment';
        setTimeout(() => {msg.innerHTML = ''}, 2000);
    } else {
        submitReview();
    }
}

function closeReviewPage() {
    rating = null;
    comment = null;
    eatery_id = null;
    for (const i of rating_set) {
        i.checked = false;
    }
    comment_input.value = null
    review_page.style.display = 'none';
}

// called when submit review button is clicked
function submitReview() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/profile/add_review', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            closeReviewPage();
            if (!this.response) {
                alert('review has submitted');
            } else {
                alert('failed to submit review');
            }
        }
    }
    xhr.send(JSON.stringify({token:token, eatery_id:eatery_id, comment:comment, rating:rating}));
}
document.onmousedown = (e) => {
    if ((!review_page.contains(e.target)) &&
        review_page.style.display === 'inline') {
        closeReviewPage();
    }
}
loadPrevious();



// function addPreviousItem(data, id) {
//     Previouss.appendChild(createItem(data, id, addDeletePreviousBtn));
// }

// function addDeletePreviousBtn(item, id) {
//     let btn = document.createElement('button');
//     btn.innerHTML = 'Delete';
//     btn.onclick = () => {
//         let xhr = new XMLHttpRequest();
//         xhr.open('DELETE', '/diner/profile/remove_previous', false);
//         xhr.setRequestHeader('Content-Type', 'application/json');
//         xhr.send(JSON.stringify({ token: token, id: id }));
//         if (!this.response) {
//             Previouss.removeChild(item);
//         } else {
//             alert('delete failed');
//         }
//     }
//     item.appendChild(btn);
// }

// get the current active page
function getCurrPage() {
    for (const p of pages) {
        if (p.style.display === 'block') {return p.id;}
    }
}


