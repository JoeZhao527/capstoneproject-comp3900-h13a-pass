// paths
const eatery_register = '/eatery/register';
const eatery_private_profile = '/eatery/profile/private';
const diner_private_profile = '/diner/profile/private';
const diner_home = '/diner/home';
const eatery_home = '/eatery/home';

// get buttons
const login_btn = document.querySelector(".login");
const sign_up_btn = document.getElementsByClassName("sign-up");
const home_btn = document.querySelector(".home");
const logout_btn = document.querySelector(".logout");
const profile_btn = document.getElementsByClassName("profile");

let token = sessionStorage.getItem('token');
let utype = sessionStorage.getItem('utype');

/* add listeners to buttons */
Array.from(sign_up_btn).forEach(element => {
    element.addEventListener('click', function() {
        window.location.href = eatery_register;
    })
})

home_btn.addEventListener('click', function() {
    window.location.href = diner_home;
})

Array.from(profile_btn).forEach(element => {
    element.addEventListener('click', function() {
        if (utype === 'diner') window.location.href = diner_private_profile;
        else window.location.href = eatery_private_profile;
    });        
});

/**
 * check if eatery logged in
 * if user logged in, show logged in page
 * otherwise show unlogged in page
 */
function loadPage() {
    token = window.sessionStorage.getItem('token');
    utype = window.sessionStorage.getItem('utype');
    console.log(token)
    if (token === 'undefined' || token === null) {
        displayDefault();
    } else {
        displayUser(token);
    }
}

// display unlogged in page
function displayDefault() {
    login_btn.style.display = 'inline';
    displaySignUp('inline');
    logout_btn.style.display = 'none';
    displayProfile('none')
}

// display logged in page
function displayUser(token) {
    console.log(token);
    console.log(sessionStorage.getItem('id'))
    login_btn.style.display = 'none';
    displaySignUp('none');
    logout_btn.style.display = 'inline';
    displayProfile('inline');
}

// set visibility of all sign up button
function displaySignUp(_display) {
    Array.from(sign_up_btn).forEach(element => {
        element.style.display = _display;
    });
}

// set visibility of all profile button
function displayProfile(_display) {
    Array.from(profile_btn).forEach(element => {
        element.style.display = _display;
    });
}

// change the text when login/logout
function displayText() {
    
}
// check user onloading
loadPage();