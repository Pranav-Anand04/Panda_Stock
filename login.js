async function logUser(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://127.0.0.1:5000/auth/login', {
        method : 'POST',
        headers: {
            'Content-Type' : 'application/json',
        },

        body: JSON.stringify({ username, password})
    });

    const result = await response.json();
    if (response.ok) {
        console.log(result.message);
        localStorage.setItem('user_id', result.user_id);
        localStorage.setItem('firstname', result.firstname);
        localStorage.setItem('username', username);
        window.location.href = 'index.html';
    } else {
        console.error(result.message);
        alert(result.message);
    }
}