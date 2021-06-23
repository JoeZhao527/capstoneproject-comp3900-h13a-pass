const add_cuisine_btn = document.getElementById('add-cuisine');
const list = document.getElementById('cuisines');
const submit_btn = document.getElementById('submit');
const form = document.forms["sign-up-form"].getElementsByTagName("input");
let cuisines = []
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
    data['cuisines'] = cuisines;
    let token = register();
    if (token) {
        sessionStorage.setItem('token', token);
        console.log('data')
        window.location.href = '../templates/eatery_home.html';
    } else {
        alert('sign up failed')
    }
    clear();
})

/**
 * use the data to check if registeration success
 */
function register() {
    JSON.stringify(data);
    // send data and receive token
    let token = 'eatery_token'
    return token;
}

/* clean up cuisines, data and inputs */
function clear() {
    cuisines = []
    data = {}
    Array.from(form).forEach(e => {
        if(e.type !== `button` && e.type !== `submit` && e.name) {
            e.value = ``;
        }
    });
    while (list.firstElementChild) { list.removeChild(list.firstElementChild) }
};

/* add cuisine */
add_cuisine_btn.addEventListener('click', function(e) {
    e.preventDefault();
    let cuisine = document.getElementById("cuisine");
    if(cuisine.value !== `` && cuisines.includes(cuisine.value) == false) {
        console.log(cuisineBtn(cuisine.value))
        list.appendChild(cuisineBtn(cuisine.value));
        cuisines.push(cuisine.value);
    }
    cuisine.value = ``;
    console.log(cuisines)
});

// cuisine tag style
const cuisine_style = "height: 2.5rem; width: 5rem; margin: 0.5rem; border: none; " + 
                    "font-family: 'Courier New', Courier, monospace;";

function cuisineListener(btn) {
    btn.addEventListener('click', function(e) {
        list.removeChild(btn);
        let idx = cuisines.indexOf(btn.innerHTML);
        if (idx > -1) { cuisines.splice(idx, 1) }
    })
}

function cuisineBtn(value) {
    let btn = document.createElement('button');
    btn.appendChild(document.createTextNode(value));
    btn.style.cssText = cuisine_style;
    
    cuisineListener(btn);
    return btn;
}

