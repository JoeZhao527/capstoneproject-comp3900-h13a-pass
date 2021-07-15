// paths
const diner_register = '/diner/register';
const diner_private_profile = '/diner/private_profile';
const diner_home = '/diner/home';
const eatery_home = '/';

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
const eatery_home_btn = document.getElementsByClassName('eatery')[0];

let data = { email: "", password: "", utype: "diner" };

/* add listeners to buttons */


Array.from(sign_up_btn).forEach(element => {
    element.addEventListener('click', function() {
        window.location.href = diner_register;
    })
})

home_btn.addEventListener('click', function() {
    window.location.href = diner_home;
})

eatery_home_btn.addEventListener('click', function() {
    window.location.href = eatery_home;
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
       window.location.href = diner_private_profile;
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
 * check if diner logged in
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
    event.preventDefault();
    Array.from(login_form).forEach(e => {
        if(e.type !== 'button' && e.type !== 'submit' && e.name) {
            data[e.name] = e.value;
        }
    });
    console.log(data);
    if (data['utype'] === 'diner') {
        diner_login();
    }
    else {
        eatery_login();
    }
}


function eatery_login() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/login', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                let res = JSON.parse(this.response);
                console.log(res);
                window.sessionStorage.setItem('token', res['token']);
                window.sessionStorage.setItem('id', res['eatery_id']);
                window.sessionStorage.setItem('utype', 'eatery');
                loadPage();
                closeLogin();
            } else {
                document.getElementById('login-msg').innerHTML = 'invalid email or password';
                login_form.reset();
                setTimeout(() => {
                    document.getElementById('login-msg').innerHTML = '';
                }, 3000);
            }
        }
    }
    xhr.send(JSON.stringify(data));
}

function diner_login() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/login', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                let res = JSON.parse(this.response);
                window.sessionStorage.setItem('token', res['token']);
                window.sessionStorage.setItem('id', res['diner_id']);
                window.sessionStorage.setItem('utype', 'diner');
                loadPage();
                closeLogin();
            } else {
                document.getElementById('login-msg').innerHTML = 'invalid email or password';
                login_form.reset();
                setTimeout(() => {
                    document.getElementById('login-msg').innerHTML = '';
                }, 3000);
            }
        }
    }
    xhr.send(JSON.stringify(data));
}


eatery_btn.onclick = () => {
    displayTab('eatery');
}

diner_btn.onclick = () => {
    displayTab('diner');
}

displayTab('diner');

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

// forgot password
const forgot_pass = document.getElementById('pass');
forgot_pass.onclick = () => {
    window.location.href = "/reset_pass"
}

const _logout = document.getElementById('logout-btn');
_logout.onclick = () => {
    if (logout()) {
        sessionStorage.removeItem('token');
        sessionStorage.removeItem('id');
        loadPage();
    } else {
        alert('logout failed');
    }
}

/**
 * send logout request to backend
 */
 function logout() {
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/logout', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(`{"token":"${sessionStorage.getItem('token')}"}`);
    return xhr.response
}

// section_style = 'width:80%; height: 200px;background-color:rgb(255, 255, 255);position:relative;left:10%;cursor: pointer;margin-bottom: 10px;'
// img_style = ''


function showEatery() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/diner/home/getEatery',true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    // console.log(xhr);
    const section_container = document.getElementById('section_container')
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let eatery_list = JSON.parse(this.response)
            console.log(eatery_list)
            console.log(eatery_list.length)
            
            for (let i = 0; i < eatery_list.length; i++) {
                eatery_detail = eatery_list[i]
                let eatery_div = document.createElement('div')
                eatery_div.className = 'section'
                // eatery_div.style = section_style

                let img = new Image()
                img.src = "../static/images/food_4.jpg"
                img.className = 'img'
                // img.style=img_style

                // let eatery_div = document.createElement('div')

                let name = document.createElement('h2')
                console.log(eatery_detail['eatery_name'])
                name.innerHTML= eatery_detail['eatery_name']
                // name.style = name_style

                let details = document.createElement('p')
                details.textContent = eatery_detail['cuisine']
                // details.style= details_style

                
                let line = document.createElement('hr')
                eatery_div.appendChild(img)
                eatery_div.appendChild(name)
                eatery_div.appendChild(details)
                eatery_div.appendChild(line)
                // eatery_div.appendChild()

                eatery_div.addEventListener('click', function() {
                    // window.location.href = /eatery/profile/${i+1};
                })

                section_container.appendChild(eatery_div)
            }
        }

    }
    xhr.send();

}
showEatery();