const book_failed_page = document.getElementById('book-failed-page');
const close_book_failed_btn = book_failed_page.getElementsByTagName('button')[0]

book_failed_page.style.visibility = 'hidden';
close_book_failed_btn.onclick = () => {
    book_failed_page.style.visibility = 'hidden';
}

document.onmousedown = (e) => {
    if ((!book_failed_page.contains(e.target)) && book_failed_page.style.visibility === 'visible') {
        book_failed_page.style.visibility = 'hidden';
    }
}

document.onmousedown = (e) => {
    if ((!login_sec.contains(e.target)) && 
        login_sec.style.display === 'inline'&&
        (!login_btn.contains(e.target))) {
        login_sec.style.display = 'none';
    }
}

function checkUser(utype, group_id) {
    if (typeof utype == 'undefined' || utype == null) {
        showLogin();
    } else if (utype == 'eatery') {
        book_failed_page.style.visibility = 'visible'
    } else {
        bookVoucher(group_id)
    }
}

function bookVoucher(voucher_id) {
    console.log(voucher_id)
    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/eatery/profile/${profile_id}/book_voucher`, true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log('here')
            if (!this.response) {
                public_loadVouchers(profile_id);
                alert('book_success')
            } else {
                alert('book_failed')
            }
        }
    }
    xhr.send(JSON.stringify({ token:token, id:user_id, group_id:voucher_id }))
}