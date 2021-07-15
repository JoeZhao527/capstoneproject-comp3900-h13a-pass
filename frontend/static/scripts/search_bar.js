const search_input = document.getElementById('search')
const search_res = document.getElementById('search-res')
const eatery_list = [
    {
        eatery_name: 'aaaaa',
        id: 1
    }
]

search_input.onkeydown = (e) => {
    if (!e.target.value) {
        search_res.innerHTML = ''
    } else {
        search_res.innerHTML = ''
        loadSearchResult(eatery_list)
    }
}

search_input.addEventListener('focusout', (e) => {
    e.target.value = ''
    search_res.innerHTML = ''
});

function searchByKeyword() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/search', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let eatery_list = JSON.parse(this.response)['data']
            loadSearchResult(eatery_list);
        }
    }
}

function loadSearchResult(eateries) {
    for (const e of eateries) {
        let eatery = document.createElement('div');
        eatery.innerHTML = e['eatery_name']
        eatery.addEventListener('mousedown', () => {
            console.log('ops')
            window.location.href = `/eatery/profile/${e['id']}`
        })
        console.log(eatery)
        search_res.appendChild(eatery)
    }
}