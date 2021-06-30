// paths
const eatery_home = "/";

// buttons
const home_btn = document.getElementById('back');
const email_form = document.getElementById('email-form');
const reset_form = document.getElementById('reset-form');
const success = document.getElementById('reset-done');
const retry = document.querySelector('.pass');

home_btn.onclick = () => {
    window.location.href = eatery_home;
}

email_form.onsubmit = (e) => {
    e.preventDefault();
    let email = email_form[0].value;

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/reset_pass', true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                let msg = document.getElementById('msg1');
                msg.innerHTML = 'invalid email';
                email_form[0].value = '';
                setTimeout(function() {
                    msg.innerHTML = '';
                }, 2000)
            } else {
                console.log('password is sent');
                displayReset();
            }
        } 
    }
    xhr.send(email)
}

reset_form.onsubmit = (e) => {
    e.preventDefault();

    // create new pass word and reset code dictionary
    let data = {}
    Array.from(reset_form).forEach(e => {
        if(e.type !== 'button' && e.type !== 'submit' && e.name) {
            data[e.name] = e.value;
        }
    });
    console.log(data)
    
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/reset_pass', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (!this.response) {
                displaySuccess();
            } else {
                let msg = document.getElementById('msg2');
                msg.innerHTML = this.response;
                reset_form[0].value = '';
                reset_form[1].value = '';
                setTimeout(function() {
                    msg.innerHTML = '';
                }, 2000)
            }
        }
    }
    xhr.send(JSON.stringify(data));
}

retry.onclick = () => {
    displayEmail();
}

success.onsubmit = (e) => {
    e.preventDefault();
    window.location.href = eatery_home;
}

function displayEmail() {
    email_form.style.display = 'block';
    reset_form.style.display = 'none';
    success.style.display = 'none';
}

function displayReset() {
    email_form.style.display = 'none';
    reset_form.style.display = 'block';
    success.style.display = 'none';
}

function displaySuccess() {
    email_form.style.display = 'none';
    reset_form.style.display = 'none';
    success.style.display = 'block';
}

displayEmail();