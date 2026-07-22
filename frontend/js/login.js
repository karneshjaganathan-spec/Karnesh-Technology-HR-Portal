document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    // If login form doesn't exist, stop execution
    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", loginUser);

});


async function loginUser(event) {

    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (username === "" || password === "") {

        showMessage(
            "Please enter username and password.",
            "error"
        );

        return;
    }

    const response = await HRAPI.post("/auth/login", {

        username: username,
        password: password

    });

    if (response.success) {

        showMessage(
            "Login Successful",
            "success"
        );

        setTimeout(() => {

            window.location.href = "dashboard.html";

        }, 1000);

    } else {

        showMessage(
            response.message,
            "error"
        );

    }

}


function showMessage(message, type) {

    let messageBox = document.getElementById("message");

    if (!messageBox) {

        messageBox = document.createElement("div");
        messageBox.id = "message";

        document
            .getElementById("loginForm")
            .prepend(messageBox);

    }

    messageBox.innerHTML = message;

    if (type === "success") {

        messageBox.style.background = "#d4edda";
        messageBox.style.color = "#155724";
        messageBox.style.border = "1px solid #c3e6cb";

    } else {

        messageBox.style.background = "#f8d7da";
        messageBox.style.color = "#721c24";
        messageBox.style.border = "1px solid #f5c6cb";

    }

    messageBox.style.padding = "12px";
    messageBox.style.marginBottom = "15px";
    messageBox.style.borderRadius = "6px";
}