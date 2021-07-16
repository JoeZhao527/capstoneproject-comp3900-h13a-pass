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

function private_loadVouchers() {
    clearVouchers();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/eatery/profile/private/get_voucher', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200 || this.status == 304) {
            voucher_list = []
            for (const data of JSON.parse(this.response)['vouchers']) {
                if (!groupVouchers(data)) {
                    // if voucher cannot be grouped with an exist one, add it to the list
                    voucher_list.push({ data: data, id: [data['id']] });
                }
            }
            for (const item of voucher_list) {
                addVoucherItem(item['data'], item['id'])
            }
        }
    }
    xhr.send(JSON.stringify({token:token}))
    // add data to schedule list
}

function clearVouchers() {
    vouchers.innerHTML = '<tr><th>date</th><th>weekday</th><th>start</th><th>end</th><th>discount</th><th>amount</th></tr>'
}

function public_loadVouchers(id) {
    voucher_container.innerHTML = '<p>No Vouchers Avaliable Today</p>';
    console.log(id);
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/eatery/profile/${id}/get_vouchers`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            voucher_list = []
            for (const data of JSON.parse(this.response)['vouchers']) {
                if (!groupVouchers(data)) {
                    // if voucher cannot be grouped with an exist one, add it to the list
                    voucher_list.push({ data: data, id: [data['id']] });
                }
            }
            for (const item of voucher_list) {
                addVoucherItem(item);
            }
            console.log(voucher_list)
        }
    }
    xhr.send()
}

if (typeof profile_id === 'undefined') {private_loadVouchers();}
else public_loadVouchers(profile_id);