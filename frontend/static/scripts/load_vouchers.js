/**
 * This file will be used in eatery public profile and eatery private profile to get 
 * eatery's vouchers, and load in apprioriate format to each file
 * 
 * Notice that the addVoucherItem() in eatery_public and eatery private is different,
 * since the required voucher format in these 2 pages are differet. For more details
 * about how vouchers get loaded to the page, see addVoucherItem in eatery_public_profile.js
 * and eatery_private_profile.js
 */

/* functionailty of grouping vouchers are moved to backend
function groupVouchers(data) {
    // incoming data is ungrouped with an item in voucher list
    let grouped = false;
    for (const voucher of voucher_list) {
        let same = true
        // for each item in the voucher list, check if the item is identical with the incoming data
        for (const [key, value] of Object.entries(voucher['data'])) {
            // the 2 data has a different attribute, the 2 items are different
            if (key !== 'code' && key !== 'id' && value !== data[key]) {
                same = false;
                break;
            }
        }
        // if a same data is found, group them, and set grouped as true
        // otherwise find the next item
        if (same) {
            voucher['id'].push(data['id'])
            grouped = true;
            break;
        }
    }
    return grouped;
}
*/
function private_loadVouchers() {
    clearVouchers();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/get_voucher', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            
            for (const data of JSON.parse(this.response)['vouchers']) {
                if (!data['schedule_id']) addVoucherItem(data, data['group_id'])
            }
        }
    }
    xhr.send(JSON.stringify({token:token}))
    // add data to schedule list
}

function clearVouchers() {
    vouchers.innerHTML = '<tr><th>date</th><th>weekday</th><th>start</th><th>end</th><th>discount</th><th>amount</th><th>Actions</th></tr>'
}

/**
 * @param {integer} id eatery's id
 * load vouchers of the eatery to /eatery/profile/${id}
 */
function public_loadVouchers(id) {
    voucher_container.innerHTML = '<p>No Vouchers Avaliable Today</p>';
    console.log(id);
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/eatery/profile/${id}/get_vouchers`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            for (const data of JSON.parse(this.response)['vouchers']) {
                // for each voucher, add it to the eatery public page
                addVoucherItem(data);
            }
        }
    }
    xhr.send()
}

if (typeof profile_id === 'undefined') {private_loadVouchers();}
else public_loadVouchers(profile_id);