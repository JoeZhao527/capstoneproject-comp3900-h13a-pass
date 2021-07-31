const to_analytic = document.getElementById('to-analysis');

function getAnalytic() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/get_analytic', true) ;
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.response) {
                res = JSON.parse(this.response)
                let line = res['line']
                let doughnut = res['doughnut']
                load_line(line);
                load_doughnut(doughnut);
            } else {
                alert('get analytics failed')
            }
        }
    }
    xhr.send(JSON.stringify({ token:token }))
}

function load_line(_data) {
    let chart = document.getElementById('line_chart')
    let labels = generateDateList();
    let data = {
        labels: labels,
        datasets: [{
            label: 'Completed Reservations in Previous Week',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: _data,
        }]
    };
    let config = {type: 'line', data, options: {}};

    let line_chart = new Chart(chart, config);
}

function load_doughnut(_data) {
    let chart = document.getElementById('doughnut_chart')
    let labels = ['1 star ', '2 star ','3 star ','4 star ','5 star '];
    let data = {
        labels: labels,
        datasets: [{
            label: 'Ratings of Reviews',
            backgroundColor: [
                'rgb(224, 54, 54)',
                'rgb(232, 175, 51)',
                'rgb(90, 188, 237)',
                'rgb(202, 111, 237)',
                'rgb(109, 237, 109)'
              ],
            data: _data,
        }]
    };
    let config = {type: 'doughnut', data, options: {}};

    let doughut_chart = new Chart(chart, config);
}

// generate previous 7 days 
function generateDateList() {
    let date_list = []
    let today = new Date();
    today.setDate(today.getDate() - 7);
    for (let i = 0; i < 7; i++) {
        // make a date 
        let dd = String(today.getDate()).padStart(2, '0'); // date
        let mm = String(today.getMonth() + 1).padStart(2, '0');  // Month
        let yyyy = today.getFullYear()
        let item = `${dd}th ${monthMap(mm)}`
        date_list.push(item);

        today.setDate(today.getDate() + 1);
    }
    return date_list;
}

// map a string like '01' to month
function monthMap(mon) {
    let month = ['Dec', 'Jun', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
    return month[parseInt(mon)]
}

// map an integer like 3 to week
function weekdayMap(w) {
    let week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    return week[w]
}

getAnalytic();