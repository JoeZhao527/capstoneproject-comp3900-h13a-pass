/* token and id */
let token = sessionStorage.getItem('token');
let id = sessionStorage.getItem('id');
let utype = sessionStorage.getItem('utype');

/* path */
const eatery_home_path = '/eatery/home';
const diner_home_path = '/diner/home';
const eatery_private_path = '/eatery/profile/private';

/* buttons */
const home_btn = document.getElementById('home-btn');
const login_btn = document.getElementById('login-btn');
const logout_btn = document.getElementById('logout-btn');
const sign_up_btn = document.getElementById('sign-up-btn')
const profile_btn = document.getElementById('profile-btn');

const user_btns = [logout_btn, profile_btn];
const default_btns = [login_btn, sign_up_btn];

/* nav bar display logic */
function loadNavBar() {
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

loadNavBar();

/* nav bar jump logic */
profile_btn.onclick = () => {
    if (utype === 'diner') window.location.href = '/diner/profile';
    else window.location.href = '/eatery/profile/private';
}

/* load image */
const image_section = document.getElementById('image-container');

/* image slide button */
const slide_right = document.getElementById('slide-right');
const slide_left = document.getElementById('slide-left');
let slide_pos = 0;

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
                if (slide_pos < pos_list.length-1) {
                    slide_pos = slide_pos + 1;
                } else {
                    //slide_pos = 0
                }
                image_section.scroll(pos_list[slide_pos], 0);
            }
            slide_left.onclick = () => {
                if (slide_pos > 0) {
                    slide_pos = slide_pos - 1;
                } else {
                    //slide_pos = pos_list.length-1
                }
                image_section.scroll(pos_list[slide_pos], 0);
            }
        }
    }
    xhr.send(JSON.stringify({token:token}))
}

getImages(id);



