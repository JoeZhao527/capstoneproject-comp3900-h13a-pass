/**
 * this file will be used to get and load reservations of the eatery
 */
const reservation_table = document.getElementById('reservation-table')
const filter = document.getElementById('filter-select');
const sorter = document.getElementById('sort-select');
const sort_order = document.getElementById('sort-order-input');
const checkcode_page = document.getElementById('checkcode-page');
const view_review_page = document.getElementById('view-review-page');
const view_detail_page = document.getElementById('view-detail-page');
const comment_container = document.getElementById('comment-container');

const close_view_detail_btn = document.getElementById('close-view-detail')
// after click complete button, the corresponding voucher id and code is stored here
let current_voucher = {}

let sort_reverse = false;

filter.onchange = () => {
    load_reservations();
}

sorter.onchange = () => {
    load_reservations();
}

sort_order.onchange = () => {
    sort_reverse = !sort_reverse;
    load_reservations();
}

function load_reservations() {
    clearReservation();
    let filter_type = filter.value
    let sort_method = sorter.value
    console.log(sort_reverse)
    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/eatery/profile/private/get_reservation/${filter_type}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let res = JSON.parse(this.response)
            for (const voucher of res['vouchers']) {
                console.log(voucher)
                addReservationItem(voucher);
            }
        }
    }
    xhr.send(JSON.stringify({token:token, sort_method:sort_method, sort_reverse:sort_reverse}))
}

function clearReservation() {
    reservation_table.innerHTML = '<tr><th>Date</th><th>Weekday</th><th>Time</th><th>Status</th><th>Discount</th><th>Contact</th><th>Action</th></tr>'
}

function addReservationItem(voucher) {
    // combine voucher time
    voucher['time'] = voucher['start_time'] + '~' + voucher['end_time']

    // make voucher status
    if (!voucher['if_used'] && !voucher['expired']) voucher['status'] = 'incomplete';
    else if (voucher['if_used'] == true) voucher['status'] = 'completed';
    else voucher['status'] = 'expired';

    // make voucher's diner contact
    voucher['contact'] = voucher['diner_name'] + ', ' + voucher['diner_phone']

    // list of table row attribute
    let row_attr = ['date', 'weekday', 'time', 'status', 'discount', 'contact']

    let tr = document.createElement('tr')
    for (const attr of row_attr) {
        let td = document.createElement('td');
        td.innerHTML = voucher[attr]
        tr.appendChild(td)
    }
    
    /* add first button */
    let btn = document.createElement('button')
    let span = document.createElement('span')
    span.className = 'tooltiptext'
    if (voucher['status'] == 'incomplete') {
        btn.className = 'complete-btn reservation-btn';
        // when click complete button, show a sub window to allow input code,
        // if the code matches, complete the booking
        btn.onclick = () => {
            checkcode_page.style.display = 'inline';
            // set code and voucher id in the variable for eatery to checkcode
            current_voucher['code'] = voucher['code']
            current_voucher['id'] = voucher['id']
        }
        span.innerHTML = "click me to enter diner's voucher code, to complete this reservation"
    } else if (voucher['status'] == 'expired') {
        btn.className = 'expire-btn reservation-btn';
        span.innerHTML = "click me to delete this expired reservation"
        btn.onclick = () => {
            deleteExpiredVoucher(voucher['id']);
            load_reservations();
        }
    } else if (voucher['status'] == 'completed') {
        btn.className = 'view-feedback-btn reservation-btn';
        btn.onclick = () => {
            view_review_page.style.display = 'inline';
            if ('reviews' in voucher) {
                loadReviews(voucher['reviews'])
            }
        }
        span.innerHTML = "click me to view diner's feed back for this reservation"
    }
    btn.appendChild(span)
    tr.appendChild(btn)

    /* add second button */
    btn = document.createElement('button')
    btn.className = 'view-detail-btn reservation-btn';
    span = document.createElement('span');
    span.className = 'tooltiptext';
    span.innerHTML = "click me to view more details of this reservation"
    btn.onclick = () => {
        view_detail_page.style.display = 'inline';
        let spans = document.getElementById('view-detail-page').getElementsByTagName('span')
        for (const item of spans) {
            item.innerHTML = voucher[item.id]
        }
    }
    btn.appendChild(span)
    tr.appendChild(btn)
    reservation_table.appendChild(tr);
}

function deleteExpiredVoucher(voucher_id) {
    let xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/eatery/profile/private/delete_voucher_by_id', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                alert('failed to delete voucher')
            }
        }
    }
    xhr.send(JSON.stringify({ token:token, voucher_id:voucher_id }))
}

function loadReviews(reviews) {
    comment_container.innerHTML = '<h3>There are No Comments For This Voucher<h3>'

    for (const rev of reviews) {
        let div = document.createElement('div');
        let p = document.createElement('p');
        let hr = document.createElement('hr')
        let starDiv = document.createElement('div');
        starDiv.className = 'Stars';
        starDiv.style = `--rating: ${rev['rating']}`;

        p.innerHTML = rev['comment']

        div.appendChild(starDiv)
        div.appendChild(p);
        div.appendChild(hr);

        comment_container.appendChild(div)
        comment_container.removeChild(comment_container.getElementsByTagName('h3')[0]);
    }
}
function completeReservation() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/complete_booking', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (!this.response) {
                load_reservations();
            } else {
                alert('complete booking failed')
            }
        }
    }
    xhr.send(JSON.stringify({token:token, voucher_id:current_voucher['id']}))
}

checkcode_page.onsubmit = (e) => {
    e.preventDefault();
    let code = document.getElementById('checkcode').value;
    if (current_voucher['code'] === code) {
        completeReservation();
    } else {
        let checkcode_msg = document.getElementById('checkcode-msg');
        checkcode_msg.innerHTML = 'code does not match';
        setTimeout(function() {
            checkcode_msg.innerHTML = '';
        }, 2000)
    }
}

load_reservations()