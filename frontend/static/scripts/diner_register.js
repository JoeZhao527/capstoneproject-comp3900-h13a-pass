// paths
const diner_home = '/diner/home';

const submit_btn = document.getElementById('submit');
const form = document.forms["sign-up-form"].getElementsByTagName("input");

const backhome = document.getElementById('back-home')
let data = {}

/* submit form */
submit_btn.addEventListener('click', function(e) {
    e.preventDefault();
    
    console.log(form)
    Array.from(form).forEach(e => {
        if(e.type !== `button` && e.type !== `submit` && e.name) {
            data[e.name] = e.value;
        }
    });
    let res = register();
    if (res !== '') {
        sessionStorage.setItem('token', res['token']);
        sessionStorage.setItem('id', res['diner_id']);
        sessionStorage.setItem('utype', 'diner');
        console.log('data')
        window.location.href = diner_home;
    } else {
        alert('sign up failed')
    }
    clear();
})
/**
 * use the data to check if registeration success
 */
function register() {
    // send data and receive token
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/diner/register', false);
    xhr.send(JSON.stringify(data))
    return JSON.parse(xhr.response);
}

/* backhome button */
backhome.addEventListener('click', function() {
    window.location.href = diner_home;
})