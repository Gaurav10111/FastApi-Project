// LOGIN
async function login() {
    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    //console.log({ email, password });

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        alert("Login successful ✅");

        window.location.href = "/qr/create-page";  // your route
    } else {
        alert("Login failed ❌");
    }
}

// TOKEN
function getToken() {
    return localStorage.getItem("token");
}

// HEADERS
function getAuthHeaders() {
    return {
        "Authorization": "Bearer " + getToken()
    };
}

// CHECK LOGIN
function checkAuth() {
    if (!getToken()) {
        alert("Please login first");
        window.location.href = "/";
    }
}