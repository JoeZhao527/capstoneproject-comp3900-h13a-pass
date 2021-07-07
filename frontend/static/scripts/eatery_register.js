// paths
const eatery_home = '/'

const add_cuisine_btn = document.getElementById('add-cuisine');
const list = document.getElementById('cuisines');
const submit_btn = document.getElementById('submit');
const form = document.forms["sign-up-form"].getElementsByTagName("input");
const backhome = document.getElementById('back-home')
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
    data['cuisines'] = cuisines.join(',');
    register();
})

/**
 * use the data to check if registeration success
 */
function register() {
    // send data and receive token
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/register', false);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                sessionStorage.setItem('token', this.response['token']);
                sessionStorage.setItem('id', this.response['eatery_id']);
                sessionStorage.setItem('utype', 'eatery');
                window.location.href = eatery_home;
            } else {
                alert('sign up failed')
            }
            clear();
        }
    }
    xhr.send(JSON.stringify(data))
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

function cuisineListener(btn) {
    let context = btn.innerHTML
    btn.onclick = () => {
        list.removeChild(btn);
        let idx = cuisines.indexOf(context);
        if (idx > -1) { cuisines.splice(idx, 1) }
    }

    btn.onmouseover = () => {
        btn.innerHTML = 'Delete';
    }

    btn.onmouseleave = () => {
        btn.innerHTML = context;
    }
}

function cuisineBtn(value) {
    let btn = document.createElement('button');
    btn.appendChild(document.createTextNode(value));
    cuisineListener(btn);
    return btn;
}

/* backhome button */
backhome.addEventListener('click', function() {
    clear();
    window.location.href = eatery_home;
})