// get buttons
const login_btn = document.querySelector(".login");
const sign_up_btn = document.getElementsByClassName("sign-up");
const home_btn = document.querySelector(".home");
const logout_btn = document.querySelector(".logout");
const profile_btn = document.getElementsByClassName("profile");
console.log(sign_up_btn[0], sign_up_btn[1])
/* add listeners to buttons */
login_btn.addEventListener('click', function() {
    window.location.href = '../templates/login.html';
})

Array.from(sign_up_btn).forEach(element => {
    element.addEventListener('click', function() {
        window.location.href = "../templates/eatery_register.html";
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
        alert('profile page is not implemented yet');
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