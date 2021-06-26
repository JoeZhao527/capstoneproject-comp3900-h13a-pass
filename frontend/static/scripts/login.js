// paths
const eatery_home = '/';

// get buttons
const diner_btn = document.getElementById("diner");
const eatery_btn = document.getElementById("eatery");
const form = document.querySelector(".form-container");
const home = document.querySelector(".back-home");

// get input and alert msg
const email = document.getElementById("email");
const password = document.getElementById("password");
const msg = document.getElementById("msg");

// styles for switch between diner and eatery
const prop = "border-bottom"
const style = "lightcoral 4px solid";

// data that will be packed up and send to server
let data = { email: "", password: "", utype: "diner" };

/* button's event listeners */
// event listener for diner button
diner_btn.addEventListener('click',function(e) {
    data.utype = "diner";
    diner_btn.style.setProperty(prop, style);
    eatery_btn.style.setProperty(prop, "none");
    console.log(data.utype);
});

// event listener for eatery button
eatery_btn.addEventListener('click',function(e) {
    data.utype = "eatery";
    eatery_btn.style.setProperty(prop, style);
    diner_btn.style.setProperty(prop, "none");
    console.log(data.utype);
});

// submit form event listener
form.addEventListener('submit', function(e) {
    e.preventDefault();
    // if there are empty field, pop an error message
    if (email.value === `` || password.value === ``) {
        msg.innerHTML = "please enter all fields";
        setTimeout(() => {
            msg.innerHTML = null;
        }, 2000);
    } else {
        // set up data
        data.email = email.value;
        data.password = password.value;
        
        let token = send(jsonData())
        if (token === null) {
            // if login or password is invalid, show an error message and clear input
            msg.innerHTML = "invalid email or password";
            setTimeout(() => {
                msg.innerHTML = null;
            }, 2000);
            clearInput();
        } else {
            // if login success, store token and direct to main
            window.sessionStorage.setItem("token", token);
            if (data.utype == "diner") {
                alert("diner login is not implemented yet");
                window.sessionStorage.removeItem("token");
            } else {
                window.location.href = eatery_home;
            }
        }
        clearInput();
    }
});

// back home event listener
home.addEventListener('click', function(e) {
    window.location.href = eatery_home
})

/* data sending and receving functions */
/**
 * :: send login data to server
 * @returns user token if login success, else false
 */
function send(data) {
    // TODO
    return "user_token"
}

/**
 * :: json stringify data
 * @returns a json string
 */
function jsonData() {
    return JSON.stringify(data);
}

/**
 * clear up input fields
 */
function clearInput() {
    email.value = ""
    password.value = ""
}