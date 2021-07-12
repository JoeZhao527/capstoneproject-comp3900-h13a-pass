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

function checkUser(utype, ids) {
    if (typeof utype == 'undefined' || utype == null) {
        showLogin();
    } else if (utype == 'eatery') {
        book_failed_page.style.visibility = 'visible'
    } else {
        alert(`vouchers with id ${ids} are avaliable`);
    }
}