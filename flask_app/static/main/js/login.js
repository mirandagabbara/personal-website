let attemptCount = 0;

function checkCredentials(event) {
    event.preventDefault(); // Prevent default form submission

    // Collect form data
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value.trim();

    // Validate inputs
    if (!email || !password) {
        showErrorMessage("Email and password are required.");
        return;
    }

    // Send data to server using fetch
    fetch("/processlogin", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ email, password }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                window.location.href = "/home";
            } else {
                attemptCount++;
                showErrorMessage(`Login failed. Attempt count: ${attemptCount}`);
            }
        })
        .catch(() => {
            showErrorMessage("An error occurred. Please try again.");
        });
}

function showErrorMessage(message) {
    const errorElement = document.getElementById("error-message");
    errorElement.textContent = message;
    errorElement.style.display = "block"; // Ensure the error message is visible
}

// Attach event listener when the page loads
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", checkCredentials);
    }
});
