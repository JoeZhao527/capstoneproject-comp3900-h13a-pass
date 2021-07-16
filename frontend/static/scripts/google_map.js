/**
 * this file is for load map in eatery public page
 */

function getAddress(addr) {
    let city = addr['city']
    let suburb = addr['suburb']
    let address = addr['address']
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `https://maps.googleapis.com/maps/api/geocode/json?address=${suburb}+${city}&key=AIzaSyAPquSqRek6F778Hr2PARZvopNtCRx2kyE`, true);
    xhr.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            res = JSON.parse(this.responseText)['results'][0]
            let lat = res['geometry']['location']['lat']
            let lng = res['geometry']['location']['lng']
            myinitMap(lat, lng, address)
        }
    }
    xhr.send()
}

// will be called by google map by default, it's here to prevent error in console
function initMap() {}

// Initialize and add the map
function myinitMap(lat, lng, address) {
    // The location of Uluru
    const addr = { lat: lat, lng: lng };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 14,
      center: addr,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: addr,
      map: map,
    });

    const infoWindow = new google.maps.InfoWindow({
        content: address
    })

    marker.addListener('click', function() {
        infoWindow.open(map, marker)
    })
}