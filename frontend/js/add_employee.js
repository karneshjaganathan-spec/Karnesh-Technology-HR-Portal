document.addEventListener("DOMContentLoaded", () => {
    checkLogin();
    loadDepartments();

    const form = document.getElementById("employeeForm");

    if (form) {
        form.addEventListener("submit", saveEmployee);
    }
});

// =====================================
// Check Login
// =====================================

async function checkLogin() {

    const response = await HRAPI.get("/auth/me");

    if (!response.logged_in) {
        window.location.href = "login.html";
    }

}

// =====================================
// Load Departments
// =====================================

async function loadDepartments() {

    const response = await HRAPI.get("/departments/");

    const department = document.getElementById("department_id");

    department.innerHTML = "";

    if (!response.success) {

        department.innerHTML =
            "<option value=''>No Departments Found</option>";

        return;
    }

    response.data.forEach(dept => {

        department.innerHTML += `

            <option value="${dept.department_id}">
                ${dept.department_name}
            </option>

        `;

    });

}

// =====================================
// Save Employee
// =====================================

async function saveEmployee(event) {

    event.preventDefault();

    const employee = {

        employee_code: document.getElementById("employee_code").value.trim(),

        first_name: document.getElementById("first_name").value.trim(),

        last_name: document.getElementById("last_name").value.trim(),

        gender: document.getElementById("gender").value,

        dob: document.getElementById("dob").value,

        email: document.getElementById("email").value.trim(),

        phone: document.getElementById("phone").value.trim(),

        address: document.getElementById("address").value.trim(),

        designation: document.getElementById("designation").value.trim(),

        salary: parseFloat(document.getElementById("salary").value),

        joining_date: document.getElementById("joining_date").value,

        department_id: parseInt(document.getElementById("department_id").value),

        user_id: parseInt(document.getElementById("user_id").value),

        status: document.getElementById("status").value

    };

    // ============================
    // Basic Validation
    // ============================

    if (
        employee.employee_code === "" ||
        employee.first_name === "" ||
        employee.last_name === ""
    ) {

        alert("Please fill all required fields.");

        return;

    }

    const response = await HRAPI.post(
    "/employees/",
    employee
);

if (response.success) {

    alert("Employee Added Successfully.");

    window.location.href = "employee.html";

} else {

    alert(response.message || "Unable to add employee.");

}

}