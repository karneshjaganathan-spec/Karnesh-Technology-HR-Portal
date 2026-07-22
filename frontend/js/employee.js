document.addEventListener("DOMContentLoaded", () => {
    checkLogin();
    loadEmployees();

    const searchInput = document.getElementById("search");

    if (searchInput) {
        searchInput.addEventListener("keyup", function (e) {
            if (e.key === "Enter") {
                searchEmployee();
            }
        });
    }
});


// ==========================================
// Check Login
// ==========================================

async function checkLogin() {

    const response = await HRAPI.get("/auth/me");

    if (!response.logged_in) {
        window.location.href = "login.html";
    }

}


// ==========================================
// Load Employees
// ==========================================

async function loadEmployees() {

    const response = await HRAPI.get("/employees/");

    if (!response.success) {

        alert(response.message);
        return;

    }

    renderTable(response.data);

}


// ==========================================
// Render Employee Table
// ==========================================

function renderTable(employees) {

    const table = document.getElementById("employeeTable");

    table.innerHTML = "";

    if (employees.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="9" class="no-data">
                    No Employees Found
                </td>
            </tr>
        `;

        return;
    }

    employees.forEach(employee => {

        table.innerHTML += `

        <tr>

            <td>${employee.employee_id}</td>

            <td>${employee.employee_code}</td>

            <td>${employee.first_name} ${employee.last_name}</td>

            <td>${employee.department_name || "-"}</td>

            <td>${employee.designation}</td>

            <td>${employee.email}</td>

            <td>${employee.phone}</td>

            <td>

                <span class="status ${employee.status.toLowerCase()}">

                    ${employee.status}

                </span>

            </td>

            <td>

                <button
                    class="action-btn edit-btn"
                    onclick="editEmployee(${employee.employee_id})">

                    <i class="fa fa-edit"></i>

                </button>

                <button
                    class="action-btn delete-btn"
                    onclick="deleteEmployee(${employee.employee_id})">

                    <i class="fa fa-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

}


// ==========================================
// Search Employee
// ==========================================

async function searchEmployee() {

    const keyword = document
        .getElementById("search")
        .value
        .trim();

    if (keyword === "") {

        loadEmployees();
        return;

    }

    const response = await HRAPI.get(

        "/employees/search?q=" +

        encodeURIComponent(keyword)

    );

    if (!response.success) {

        alert(response.message);
        return;

    }

    renderTable(response.data);

}


// ==========================================
// Delete Employee
// ==========================================

async function deleteEmployee(employeeId) {

    const ok = confirm(

        "Are you sure you want to delete this employee?"

    );

    if (!ok)
        return;

    const response = await HRAPI.delete(

        "/employees/" + employeeId

    );

    if (response.success) {

        alert("Employee deleted successfully.");

        loadEmployees();

    } else {

        alert(response.message);

    }

}


// ==========================================
// Edit Employee
// ==========================================

function editEmployee(employeeId) {

    window.location.href =

        "edit_employee.html?id=" + employeeId;

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    const response = await HRAPI.post(

        "/auth/logout",

        {}

    );

    if (response.success) {

        window.location.href = "login.html";

    }

}
// ==========================================
// Export Excel
// ==========================================

function exportExcel(){

    window.open(

        `${HRAPI.baseURL}/export/employees/excel`,

        "_blank"

    );

}


// ==========================================
// Export PDF
// ==========================================

function exportPDF(){

    window.open(

        `${HRAPI.baseURL}/export/employees/pdf`,

        "_blank"

    );

}