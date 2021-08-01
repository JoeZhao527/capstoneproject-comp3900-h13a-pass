// paths
const diner_home = '/diner/home';

const submit_btn = document.getElementById('submit');
const form = document.forms["sign-up-form"].getElementsByTagName("input");
const signup_form = document.getElementById('sign-up-form');

const backhome = document.getElementById('back-home')
let data = {}

/* submit form */
signup_form.onsubmit = (e) => {
    e.preventDefault()
    Array.from(form).forEach(e => {
        if(e.type !== `button` && e.type !== `submit` && e.name) {
            data[e.name] = e.value;
        }
    });
    
    register();
}
/**
 * use the data to check if registeration success
 */
function register() {
    // send data and receive token
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/register', false);
    xhr.onreadystatechange = function() {
        let res = this.response
        if (isJson(res)) {
            res = JSON.parse(res)
            sessionStorage.setItem('token', res['token']);
            sessionStorage.setItem('id', res['diner_id']);
            sessionStorage.setItem('utype', 'diner');
            console.log('data')
            window.location.href = diner_home;
        } else {
            let sign_up_msg = document.getElementById('signup-msg');
                sign_up_msg.innerHTML = this.response
                setTimeout(() => {
                    sign_up_msg.innerHTML = ''
                }, 3000)
        }
        clear();
    }
    xhr.send(JSON.stringify(data))
    return JSON.parse(xhr.response);
}

/* backhome button */
backhome.addEventListener('click', function() {
    window.location.href = diner_home;
})

function isJson(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}
