/* main and nav bar*/
const main = document.getElementById('main');
const nav_bar = document.getElementById('nav-bar');

// debug line
console.log(sessionStorage.getItem('token'));

/* eatery profile info */
const info_item = document.getElementById('eatery-info').getElementsByTagName('li');

// get eatery's info by its token
function getEateryData() {
    let token = sessionStorage.getItem('token');
    let _data = {
        fname: 'joe',
        lname: 'zhao',
        ename: 'eatery_name',
        email: '1016859319@qq.com',
        phone: '0452568128',
        address: 'address, 2052 UNSW',
    }
    return _data
}

// load eatery data to profile
function loadEateryData(_data) {
    Array.from(info_item).forEach(e => {
        e.innerHTML = e.innerHTML+'\xa0\xa0\xa0\xa0\xa0'+_data[e.id]
    });
}

let data = getEateryData();
loadEateryData(data);

/* buttons */
// diner home page
const home_btn = document.getElementById('home');
home_btn.addEventListener('click', function() {
    alert('diner home page not implmented yet');
});

// logout
const logout_btn = document.getElementById('logout');
logout_btn.addEventListener('click', function() {
    sessionStorage.removeItem('token');
    window.location.href = '../templates/eatery_home.html';
})

// back eatery home
const back_btn = document.getElementById('back');
back_btn.onclick = () => {
    window.location.href = '../templates/eatery_home.html';
}

/* edit profile */
const edit_btn = document.getElementById('edit-profile');
const edit_page = document.getElementById('edit-page');

edit_btn.onclick = () => {
    openSubpage(edit_page)
};

const close_edit = edit_page.getElementsByClassName('close')[0];
console.log(close_edit)

// close subpage
function closeSubpage(page) {
    page.style.display = 'none';
    main.style.display = 'inline';
    nav_bar.style.display = 'inline';
}

// open subpage
function openSubpage(page) {
    page.style.display = 'inline';
    main.style.display = 'none';
    nav_bar.style.display = 'none';
}

close_edit.onclick = () => {
    closeSubpage(edit_page);
}
