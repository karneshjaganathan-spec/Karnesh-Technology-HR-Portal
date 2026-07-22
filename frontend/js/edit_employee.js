let employeeId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    const params = new URLSearchParams(window.location.search);
    employeeId = params.get("id");

    if (!employeeId) {
        alert("Employee ID not found.");
        window.location.href = "employee.html";
        return;
    }

    loadDepartments();
    loadEmployee();

    document
        .getElementById("editEmployeeForm")
        .addEventListener("submit", updateEmployee);

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
// Load Departments
// ======================================

async function loadDepartments() {

    const response = await HRAPI.get("/departments/");

    if (!response.success)
        return;

    const select = document.getElementById("department_id");

    select.innerHTML = "";

    response.data.forEach(department => {

        select.innerHTML += `

            <option value="${department.department_id}">
                ${department.department_name}
            </option>

        `;

    });

}


// ======================================
// Load Employee Details
// ======================================

async function loadEmployee() {

    const response = await HRAPI.get(

        "/employees/" + employeeId

    );

    if (!response.success) {

        alert(response.message);

        return;

    }

    const employee = response.data;

    document.getElementById("employee_code").value = employee.employee_code;
    document.getElementById("first_name").value = employee.first_name;
    document.getElementById("last_name").value = employee.last_name;
    document.getElementById("gender").value = employee.gender;
    document.getElementById("dob").value = employee.dob;
    document.getElementById("email").value = employee.email;
    document.getElementById("phone").value = employee.phone;
    document.getElementById("address").value = employee.address;
    document.getElementById("designation").value = employee.designation;
    document.getElementById("salary").value = employee.salary;
    document.getElementById("joining_date").value = employee.joining_date;
    document.getElementById("department_id").value = employee.department_id;
    document.getElementById("user_id").value = employee.user_id;
    document.getElementById("status").value = employee.status;

}


// ======================================
// Update Employee
// ======================================

async function updateEmployee(event) {

    event.preventDefault();

    const employee = {

        employee_code:
            document.getElementById("employee_code").value.trim(),

        first_name:
            document.getElementById("first_name").value.trim(),

        last_name:
            document.getElementById("last_name").value.trim(),

        gender:
            document.getElementById("gender").value,

        dob:
            document.getElementById("dob").value,

        email:
            document.getElementById("email").value.trim(),

        phone:
            document.getElementById("phone").value.trim(),

        address:
            document.getElementById("address").value.trim(),

        designation:
            document.getElementById("designation").value.trim(),

        salary:
            parseFloat(document.getElementById("salary").value),

        joining_date:
            document.getElementById("joining_date").value,

        department_id:
            parseInt(document.getElementById("department_id").value),

        user_id:
            parseInt(document.getElementById("user_id").value),

        status:
            document.getElementById("status").value

    };

    const response = await HRAPI.put(

        "/employees/" + employeeId,

        employee

    );

    if (response.success) {

        alert("Employee Updated Successfully.");

        window.location.href = "employee.html";

    } else {

        alert(response.message);

    }

}