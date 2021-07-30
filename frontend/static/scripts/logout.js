/* logout */
const _logout = document.getElementById('logout-btn');
_logout.onclick = () => {
    if (logout()) {
        sessionStorage.removeItem('token');
        sessionStorage.removeItem('id');
        sessionStorage.removeItem('utype');
        window.location.href = '/';
    } else {
        alert('logout failed');
    }
}

/**
 * send logout request to backend
 */
 function logout() {
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', '/logout', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(`{"token":"${sessionStorage.getItem('token')}"}`);
    return xhr.response
}