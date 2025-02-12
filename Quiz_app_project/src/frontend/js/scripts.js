document.getElementById('login-btn').addEventListener('click', function() {
    showForm('login');
});

document.getElementById('register-btn').addEventListener('click', function() {
    showForm('register');
});

function showForm(type) {
    const formContainer = document.getElementById('form-container');
    formContainer.innerHTML = '';

    if (type === 'login') {
        formContainer.innerHTML = `
            <form id="login-form">
                <input type="text" id="login-username" placeholder="Username" required>
                <input type="password" id="login-password" placeholder="Password" required>
                <select id="login-role">
                    <option value="admin">Admin</option>
                    <option value="candidate">Candidate</option>
                </select>
                <button type="submit">Login</button>
            </form>
        `;
        document.getElementById('login-form').addEventListener('submit', handleLogin);
    } else if (type === 'register') {
        formContainer.innerHTML = `
            <form id="register-form">
                <input type="text" id="register-username" placeholder="Username" required>
                <input type="password" id="register-password" placeholder="Password" required>
                <select id="register-role">
                    <option value="admin">Admin</option>
                    <option value="candidate">Candidate</option>
                </select>
                <button type="submit">Register</button>
            </form>
        `;
        document.getElementById('register-form').addEventListener('submit', handleRegister);
    }

    document.getElementById(`${type}-form`).style.display = 'block';
}

async function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const role = document.getElementById('register-role').value;

    const response = await fetch('http://127.0.0.1:8000/v1/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, role })
    });

    if (response.ok) {
        alert('Registration successful!');
    } else {
        alert('Registration failed!');
    }
}

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const role = document.getElementById('login-role').value;

    const response = await fetch('http://127.0.0.1:8000/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        const token = data.access_token;

        // Store the token in localStorage
        localStorage.setItem('token', token);

        // Redirect based on role
        if (role === 'admin') {
            window.location = './admin.html';
        } else if (role === 'candidate') {
            window.location = './candidate.html';
        }
    } else {
        alert('Login failed!');
    }
}