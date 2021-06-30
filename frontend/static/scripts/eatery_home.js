// paths
const eatery_register = '/eatery/register';
const eatery_private_profile = '/eatery_private_profile';

// get buttons
const login_btn = document.querySelector(".login");
const sign_up_btn = document.getElementsByClassName("sign-up");
const home_btn = document.querySelector(".home");
const logout_btn = document.querySelector(".logout");
const profile_btn = document.getElementsByClassName("profile");

const login_sec = document.getElementById('login-page');
const login_form = document.getElementById('login-form');
const eatery_btn = document.getElementById('eatery');
const diner_btn = document.getElementById('diner');

let data = { email: "", password: "", utype: "eatery" };

/* add listeners to buttons */
Array.from(sign_up_btn).forEach(element => {
    element.addEventListener('click', function() {
        window.location.href = eatery_register;
    })
})

home_btn.addEventListener('click', function() {
    alert("diner home is not implemented yet");
})

logout_btn.addEventListener('click', function() {
    if (logout()) {
        window.sessionStorage.removeItem('token');
        loadPage();
    } else {
        alert('logout failed for unknown reason');
    }
})

Array.from(profile_btn).forEach(element => {
    element.addEventListener('click', function() {
       window.location.href = eatery_private_profile;
    });        
});

/**
 * send logout request to backend
 */
function logout() {
    let token = window.sessionStorage.getItem('token');
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/logout', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(`{"token":"${token}"}`);
    console.log(xhr.response);
    return xhr.response
}


/**
 * check if eatery logged in
 * if user logged in, show logged in page
 * otherwise show unlogged in page
 */
function loadPage() {
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
loadPage();

/* login form */
login_btn.addEventListener('click', function() {
    //window.location.href = '/login';
    showLogin();
})

document.onmousedown = (e) => {
    if ((!login_sec.contains(e.target)) && 
        login_sec.style.display === 'inline'&&
        (!login_btn.contains(e.target))) {
        login_sec.style.display = 'none';
    }
}

login_form.onsubmit = (event) => {
    Array.from(login_form).forEach(e => {
        if(e.type !== 'button' && e.type !== 'submit' && e.name) {
            data[e.name] = e.value;
        }
    });
    console.log(data);
    if (data['utype'] === 'diner') {alert('diner is not implemented yet')}
    else {
        let token = login();
        if (token) {
            window.sessionStorage.setItem('token', token);
        } else {
            alert('login failed');
        }
        loadPage();
    }
    closeLogin();
}

function login() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'login', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    return xhr.response;
}

eatery_btn.onclick = () => {
    displayTab('eatery');
}

diner_btn.onclick = () => {
    displayTab('diner');
}

displayTab('eatery');

function displayTab(user) {
    if (user === 'diner') {
        diner_btn.style.setProperty('border-bottom', '#2691d9 3px solid');
        eatery_btn.style.setProperty('border-bottom', 'none');
        data['utype'] = 'diner'
    } else {
        eatery_btn.style.setProperty('border-bottom', '#2691d9 3px solid');
        diner_btn.style.setProperty('border-bottom', 'none');
        data['utype'] = 'eatery'
    }
}

function closeLogin() {
    login_sec.style.display = 'none';
}

function showLogin() {
    login_sec.style.display = 'inline';
}