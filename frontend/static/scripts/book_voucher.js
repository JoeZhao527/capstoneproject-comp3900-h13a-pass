const book_failed_page = document.getElementById('book-failed-page');
const close_book_failed_btn = book_failed_page.getElementsByTagName('button')[0]
const book_info_section = document.getElementById('book-enter-info');
const book_info_form = document.getElementById('book-info-form');

book_failed_page.style.visibility = 'hidden';
close_book_failed_btn.onclick = () => {
    book_failed_page.style.visibility = 'hidden';
}

document.onclick = (e) => {
    console.log(book_info_section.style.display == 'inline')
    
}

document.onmousedown = (e) => {
    if ((!login_sec.contains(e.target)) && 
        login_sec.style.display === 'inline'&&
        (!login_btn.contains(e.target))) {
        login_sec.style.display = 'none';
    }
    if ((!book_failed_page.contains(e.target)) && book_failed_page.style.visibility === 'visible') {
        book_failed_page.style.visibility = 'hidden';
    }
    if ((!book_info_section.contains(e.target)) && book_info_section.style.display == 'inline') {
        book_info_section.style.display = 'none';
        for (const input of book_info_form.elements) {
            if (input.type != 'submit') input.value = '';
        }
    }
    if (!menu_section.contains(e.target) && menu_section.style.display == 'inline') {
        menu_section.style.display = 'none';
    }
}

function checkUser(utype, group_id) {
    if (typeof utype == 'undefined' || utype == null) {
        showLogin();
    } else if (utype == 'eatery') {
        book_failed_page.getElementsByTagName('h2')[0].innerHTML = 'Only diner can book vouchers!';
        book_failed_page.style.visibility = 'visible';
    } else {
        showBookInfo(group_id);
        //bookVoucher(group_id)
    }
}

function bookVoucher(voucher_id) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/eatery/profile/${profile_id}/book_voucher`, false);
    xhr.send(JSON.stringify({ 
        token:token, 
        id:user_id, 
        group_id:voucher_id, 
        arrival_time:book_data['arrival_time'], 
        number_of_people:book_data['number_of_people'],
        request:book_data['additional_request']
    }))

    if (!xhr.response) {
        public_loadVouchers(profile_id);
    } else {
        book_failed_page.getElementsByTagName('h2')[0].innerHTML = 'You have already booked this voucher!';
        book_failed_page.style.visibility = 'visible';
    }
    book_info_section.style.display = 'none';
}

let book_data = {}

/* book voucher enter info page */
function showBookInfo(group_id) {
    book_info_section.style.display = 'inline';
    book_info_form.onsubmit = (e) => {
        for (const input of book_info_form.elements) {
            book_data[input.name] = input.value
        }
        bookVoucher(group_id)
        for (const input of book_info_form.elements) {
            if (input.type != 'submit') input.value = '';
        }
        return false
    }
}
