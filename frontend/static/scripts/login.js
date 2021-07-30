/* login form */
const login_sec = document.getElementById('login-page');
const login_form = document.getElementById('login-form');
const eatery_btn = document.getElementById('eatery');
const diner_btn = document.getElementById('diner');

let data = { email: "", password: "", utype: "eatery" };

login_btn.addEventListener('click', function() {
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
    // clear up login form
    Array.from(login_form).forEach(e => {
        if(e.type !== 'button' && e.type !== 'submit' && e.name) {
            e.value = '';
        }
    });
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
    xhr.open('POST', '/diner/login', true);
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

displayTab('eatery');

function displayTab(user) {
    if (user === 'diner') {
        diner_btn.style.setProperty('border-bottom', '#2691d9 2px solid');
        eatery_btn.style.setProperty('border-bottom', 'none');
        data['utype'] = 'diner'
    } else {
        eatery_btn.style.setProperty('border-bottom', '#2691d9 2px solid');
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