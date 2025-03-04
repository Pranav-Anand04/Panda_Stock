// Create user function
async function createUser(e) {
    // Prevent form reload on submit
    e.preventDefault();

    // Get form data
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;

    // Make API request to the backend, this is connected to local host but has 
    // to be changed to the website when we create one. :)
    const response = await fetch('http://127.0.0.1:5000/auth/register', {
        method: 'POST',
        // This tells what the content is 
        headers: {
            'Content-Type': 'application/json',
        },
        // this just gets the value make it to object and sends them over to the register backend
        body: JSON.stringify({ username, password, firstname, lastname }),
    });

    // just to see what respose we will get from backend
    // Specifically converts the backend message to json so we can see in JS
    const result = await response.json();

    // Handle response
    // Response is good then we would like to see in cosole and alert.
    console.log("Going to response ok");
    if (response.ok) {
        console.log(result.message);
        // Set timeout to create the real world load page
        // We could create an HTML where it can show loading screen
        localStorage.setItem('username', username);
        window.location.href = 'index.html';
    } else {
        // If not ok show message
        // Might need to show a message when the user already exist. 
        console.error(result.message);
        alert(result.message);
    }
}
