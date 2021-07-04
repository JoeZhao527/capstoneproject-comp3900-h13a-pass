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
    let token = register();
    if (token !== '') {
        sessionStorage.setItem('token', token);
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
    xhr.open('POST', '/dinner/register', false);
    xhr.send(JSON.stringify(data))
    return xhr.response;
}

/* backhome button */
backhome.addEventListener('click', function() {
    window.location.href = diner_home;
})