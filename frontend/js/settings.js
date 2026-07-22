document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadSettings();

    document
        .getElementById("settingsForm")
        .addEventListener("submit", saveSettings);

});


// ==========================================
// Check Login
// ==========================================

async function checkLogin(){

    const response = await HRAPI.get("/auth/me");

    if(!response.logged_in){

        window.location.href = "login.html";

    }

}


// ==========================================
// Load Settings
// ==========================================

async function loadSettings(){

    const response = await HRAPI.get("/settings/");

    if(!response.success)
        return;

    const s = response.data;

    document.getElementById("company_name").value =
        s.company_name || "";

    document.getElementById("company_email").value =
        s.company_email || "";

    document.getElementById("company_phone").value =
        s.company_phone || "";

    document.getElementById("company_address").value =
        s.company_address || "";

    document.getElementById("company_website").value =
        s.company_website || "";

    document.getElementById("working_hours_start").value =
        s.working_hours_start || "";

    document.getElementById("working_hours_end").value =
        s.working_hours_end || "";

    document.getElementById("leave_per_year").value =
        s.leave_per_year || 12;

    document.getElementById("currency").value =
        s.currency || "INR";

    document.getElementById("timezone").value =
        s.timezone || "Asia/Kolkata";

}


// ==========================================
// Save Settings
// ==========================================

async function saveSettings(event){

    event.preventDefault();

    const settings = {

        company_name:
            document.getElementById("company_name").value,

        company_email:
            document.getElementById("company_email").value,

        company_phone:
            document.getElementById("company_phone").value,

        company_address:
            document.getElementById("company_address").value,

        company_website:
            document.getElementById("company_website").value,

        working_hours_start:
            document.getElementById("working_hours_start").value,

        working_hours_end:
            document.getElementById("working_hours_end").value,

        leave_per_year:
            Number(
                document.getElementById("leave_per_year").value
            ),

        currency:
            document.getElementById("currency").value,

        timezone:
            document.getElementById("timezone").value

    };

    const response = await HRAPI.put(

        "/settings/",

        settings

    );

    if(response.success){

        alert("Settings updated successfully.");

    }

    else{

        alert(response.message);

    }

}


// ==========================================
// Logout
// ==========================================

async function logout(){

    await HRAPI.post("/auth/logout",{});

    window.location.href="login.html";

}