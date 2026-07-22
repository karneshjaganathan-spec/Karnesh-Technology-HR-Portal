document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadProfile();

    document
        .getElementById("profileForm")
        .addEventListener("submit", updateProfile);

    document
        .getElementById("passwordForm")
        .addEventListener("submit", changePassword);

});


// ======================================
// Check Login
// ======================================

async function checkLogin() {

    const response = await HRAPI.get("/auth/me");

    if (!response.logged_in) {

        window.location.href = "login.html";

    }

}


// ======================================
// Load Profile
// ======================================

async function loadProfile() {

    const response = await HRAPI.get("/profile/");

    if (!response.success) {

        alert(response.message);
        return;

    }

    const profile = response.data;

    document.getElementById("fullName").innerText =
        profile.first_name + " " + profile.last_name;

    document.getElementById("designation").innerText =
        profile.designation;

    document.getElementById("roleBadge").innerText =
        profile.role_name;

    document.getElementById("employee_code").value =
        profile.employee_code;

    document.getElementById("department").value =
        profile.department_name;

    document.getElementById("email").value =
        profile.email || "";

    document.getElementById("phone").value =
        profile.phone || "";

    document.getElementById("address").value =
        profile.address || "";

}


// ======================================
// Update Profile
// ======================================

async function updateProfile(event) {

    event.preventDefault();

    const profile = {

        email:
            document.getElementById("email").value.trim(),

        phone:
            document.getElementById("phone").value.trim(),

        address:
            document.getElementById("address").value.trim()

    };

    const response = await HRAPI.put(

        "/profile/",

        profile

    );

    if (response.success) {

        alert("Profile Updated Successfully.");

    }
    else {

        alert(response.message);

    }

}


// ======================================
// Change Password
// ======================================

async function changePassword(event) {

    event.preventDefault();

    const data = {

        current_password:
            document.getElementById("current_password").value,

        new_password:
            document.getElementById("new_password").value,

        confirm_password:
            document.getElementById("confirm_password").value

    };

    if (data.new_password !== data.confirm_password) {

        alert("Passwords do not match.");

        return;

    }

    const response = await HRAPI.put(

        "/profile/change-password",

        data

    );

    if (response.success) {

        alert("Password Changed Successfully.");

        document
            .getElementById("passwordForm")
            .reset();

    }
    else {

        alert(response.message);

    }

}


// ======================================
// Logout
// ======================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}