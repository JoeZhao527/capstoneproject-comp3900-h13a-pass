// paths
const eatery_register = '/eatery/register';
const eatery_private_profile = '/eatery_private_profile';

// get buttons
const login_btn = document.querySelector(".login");
const sign_up_btn = document.getElementsByClassName("sign-up");
const home_btn = document.querySelector(".home");
const logout_btn = document.querySelector(".logout");
const profile_btn = document.getElementsByClassName("profile");

/* add listeners to buttons */
login_btn.addEventListener('click', function() {
    window.location.href = '/login';
})

Array.from(sign_up_btn).forEach(element => {
    element.addEventListener('click', function() {
        window.location.href = eatery_register;
    })
})

home_btn.addEventListener('click', function() {
    alert("diner home is not implemented yet");
})

logout_btn.addEventListener('click', function() {
    window.sessionStorage.removeItem('token');
    checkUser();
})

Array.from(profile_btn).forEach(element => {
    element.addEventListener('click', function() {
       window.location.href = eatery_private_profile;
    });        
});


/**
 * check if eatery logged in
 * if user logged in, show logged in page
 * otherwise show unlogged in page
 */
function checkUser() {
    let token = window.sessionStorage.getItem('token')
    if (token === null) {
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
checkUser();

const turn_description_btn = document.getElementById("description-btn")
const turn_menu_btn = document.getElementById('menu-btn');
const turn_details_btn = document.getElementById('details-btn');

const description = document.getElementById('description');
const menu = document.getElementById('menu');
const eaterydetails = document.getElementById('eaterydetails');

function displayDescriptionList() {
    turn_description_btn.style.setProperty('border-bottom', 'white 4px solid');
    turn_menu_btn.style.setProperty('border-bottom', 'none');
    turn_details_btn.style.setProperty('border-bottom', 'none');
    description.style.display = 'inline';
    menu.style.display = 'none';
    eaterydetails.style.display = 'none';
}

function displayMenuList() {
    turn_description_btn.style.setProperty('border-bottom', 'none');
    turn_menu_btn.style.setProperty('border-bottom', 'white 4px solid');
    turn_details_btn.style.setProperty('border-bottom', 'none');
    description.style.display = 'none';
    menu.style.display = 'inline';
    eaterydetails.style.display = 'none';
}

function displayDetailsList() {
    turn_description_btn.style.setProperty('border-bottom', 'none');
    turn_menu_btn.style.setProperty('border-bottom', 'none');
    turn_details_btn.style.setProperty('border-bottom', 'white 4px solid');
    description.style.display = 'none';
    menu.style.display = 'none';
    eaterydetails.style.display = 'inline';
}

turn_description_btn.onclick = () => {
    displayDescriptionList();
}

turn_menu_btn.onclick = () => {
    displayMenuList();
}

turn_details_btn.onclick = () => {
    displayDetailsList();
}

displayDescriptionList();


const turn_breakfast_btn = document.getElementById("Breakfast-btn")
const turn_lunch_btn = document.getElementById('Lunch-btn');
const turn_dinner_btn = document.getElementById('Dinner-btn');

const breakfast = document.getElementById('breakfast');
const lunch = document.getElementById('lunch');
const dinner = document.getElementById('dinner');

function displayBreakfastList() {
    turn_breakfast_btn.style.setProperty('border-bottom', 'white 4px solid');
    turn_lunch_btn.style.setProperty('border-bottom', 'none');
    turn_dinner_btn.style.setProperty('border-bottom', 'none');
    breakfast.style.display = 'inline';
    lunch.style.display = 'none';
    dinner.style.display = 'none';
}

function displayLunchList() {
    turn_breakfast_btn.style.setProperty('border-bottom', 'none');
    turn_lunch_btn.style.setProperty('border-bottom', 'white 4px solid');
    turn_dinner_btn.style.setProperty('border-bottom', 'none');
    breakfast.style.display = 'none';
    lunch.style.display = 'inline';
    dinner.style.display = 'none';
}

function displayDinnerList() {
    turn_breakfast_btn.style.setProperty('border-bottom', 'none');
    turn_lunch_btn.style.setProperty('border-bottom', 'none');
    turn_dinner_btn.style.setProperty('border-bottom', 'white 4px solid');
    breakfast.style.display = 'none';
    lunch.style.display = 'none';
    dinner.style.display = 'inline';
}

turn_breakfast_btn.onclick = () => {
    displayBreakfastList();
}

turn_lunch_btn.onclick = () => {
    displayLunchList();
}

turn_dinner_btn.onclick = () => {
    displayDinnerList();
}

displayBreakfastList();