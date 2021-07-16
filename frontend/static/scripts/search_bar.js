const search_input = document.getElementById('search')
const search_res = document.getElementById('search-res')

search_input.onkeydown = (e) => {
    if (!e.target.value) {
        search_res.innerHTML = ''
    } else {
        search_res.innerHTML = ''
        searchByKeyword(e.target.value);
    }
}

search_input.addEventListener('focusout', (e) => {
    e.target.value = ''
    search_res.innerHTML = ''
});

function searchByKeyword(keyword) {
    console.log('here')
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/search', true);
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let eatery_list = JSON.parse(this.response)['data']
            console.log(eatery_list)
            loadSearchResult(eatery_list);
        }
    }
    xhr.send(JSON.stringify({keyword:keyword}))
}

function loadSearchResult(eateries) {
    for (const e of eateries) {
        let eatery = document.createElement('div');
        eatery.innerHTML = e['eatery_name']
        eatery.addEventListener('mousedown', () => {
            window.location.href = `/eatery/profile/${e['id']}`
        })
        console.log(eatery)
        search_res.appendChild(eatery)
    }
}