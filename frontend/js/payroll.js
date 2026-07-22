let payrollId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadSummary();

    loadPayroll();

    loadEmployees();

    document
        .getElementById("payrollForm")
        .addEventListener("submit", savePayroll);

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
// Load Payroll Summary
// ==========================================

async function loadSummary() {

    const response = await HRAPI.get("/payroll/summary");

    if (!response.success)
        return;

    const data = response.data;

    document.getElementById("employeeCount").innerText =
        data.total_employees || 0;

    document.getElementById("totalPayroll").innerText =
        "₹ " + Number(data.total_salary || 0).toLocaleString();

    document.getElementById("averageSalary").innerText =
        "₹ " + Number(data.average_salary || 0).toLocaleString();

}


// ==========================================
// Load Payroll Records
// ==========================================

async function loadPayroll() {

    const response = await HRAPI.get("/payroll/");

    if (!response.success)
        return;

    renderPayroll(response.data);

}


// ==========================================
// Render Payroll Table
// ==========================================

function renderPayroll(records) {

    const table = document.getElementById("payrollTable");

    table.innerHTML = "";

    if (records.length === 0) {

        table.innerHTML = `

        <tr>

            <td colspan="10">

                No Payroll Records Found

            </td>

        </tr>

        `;

        return;

    }

    records.forEach(record => {

        let badge =
            record.status === "Paid"
            ? "paid"
            : "pending";

        table.innerHTML += `

        <tr>

            <td>${record.payroll_id}</td>

            <td>

                ${record.employee_code}

                -

                ${record.first_name}

                ${record.last_name}

            </td>

            <td>${record.designation}</td>

            <td>₹ ${record.basic_salary}</td>

            <td>₹ ${record.allowances}</td>

            <td>₹ ${record.deductions}</td>

            <td>

                ₹ ${record.net_salary}

            </td>

            <td>${record.pay_month}</td>

            <td>

                <span class="badge ${badge}">

                    ${record.status}

                </span>

            </td>

            <td>

                <button
                    class="action-btn edit-btn"
                    onclick="editPayroll(${record.payroll_id})">

                    <i class="fa fa-edit"></i>

                </button>

                <button
                    class="action-btn delete-btn"
                    onclick="deletePayroll(${record.payroll_id})">

                    <i class="fa fa-trash"></i>

                </button>

                <button
                    class="action-btn print-btn"
                    onclick="printSlip(${record.payroll_id})">

                    <i class="fa fa-print"></i>

                </button>

            </td>

        </tr>

        `;

    });

}


// ==========================================
// Load Employee Dropdown
// ==========================================

async function loadEmployees() {

    const response = await HRAPI.get("/employees/");

    if (!response.success)
        return;

    const employee = document.getElementById("employee_id");

    employee.innerHTML = "";

    response.data.forEach(emp => {

        employee.innerHTML += `

            <option
                value="${emp.employee_id}">

                ${emp.employee_code}

                -

                ${emp.first_name}

                ${emp.last_name}

            </option>

        `;

    });

}


// ==========================================
// Save Payroll
// ==========================================

async function savePayroll(event) {

    event.preventDefault();

    const payroll = {

        employee_id:
            parseInt(document.getElementById("employee_id").value),

        basic_salary:
            Number(document.getElementById("basic_salary").value),

        allowances:
            Number(document.getElementById("allowances").value),

        deductions:
            Number(document.getElementById("deductions").value),

        pay_month:
            document.getElementById("pay_month").value,

        payment_date:
            document.getElementById("payment_date").value,

        status:
            document.getElementById("status").value

    };

    const response = await HRAPI.post(

        "/payroll/",

        payroll

    );

    if (response.success) {

        alert("Payroll Generated Successfully.");

        closePayrollModal();

        document
            .getElementById("payrollForm")
            .reset();

        loadPayroll();

        loadSummary();

    }
    else {

        alert(response.message);

    }

}


// ==========================================
// Edit Payroll
// ==========================================

async function editPayroll(id) {

    payrollId = id;

    const response = await HRAPI.get(

        "/payroll/" + id

    );

    if (!response.success)
        return;

    const payroll = response.data;

    document.getElementById("employee_id").value =
        payroll.employee_id;

    document.getElementById("basic_salary").value =
        payroll.basic_salary;

    document.getElementById("allowances").value =
        payroll.allowances;

    document.getElementById("deductions").value =
        payroll.deductions;

    document.getElementById("pay_month").value =
        payroll.pay_month;

    document.getElementById("payment_date").value =
        payroll.payment_date;

    document.getElementById("status").value =
        payroll.status;

    openPayrollModal();

    document
        .getElementById("payrollForm")
        .onsubmit = updatePayroll;

}


// ==========================================
// Update Payroll
// ==========================================

async function updatePayroll(event) {

    event.preventDefault();

    const payroll = {

        basic_salary:
            Number(document.getElementById("basic_salary").value),

        allowances:
            Number(document.getElementById("allowances").value),

        deductions:
            Number(document.getElementById("deductions").value),

        pay_month:
            document.getElementById("pay_month").value,

        payment_date:
            document.getElementById("payment_date").value,

        status:
            document.getElementById("status").value

    };

    const response = await HRAPI.put(

        "/payroll/" + payrollId,

        payroll

    );

    if (response.success) {

        alert("Payroll Updated.");

        closePayrollModal();

        loadPayroll();

        loadSummary();

    }

}


// ==========================================
// Delete Payroll
// ==========================================

async function deletePayroll(id) {

    if (!confirm("Delete payroll?"))
        return;

    const response = await HRAPI.delete(

        "/payroll/" + id

    );

    if (response.success) {

        loadPayroll();

        loadSummary();

    }

}


// ==========================================
// Month Filter
// ==========================================

function filterPayroll() {

    const month =
        document.getElementById("payMonth").value;

    const rows =
        document.querySelectorAll("#payrollTable tr");

    rows.forEach(row => {

        if (month === "") {

            row.style.display = "";

            return;

        }

        row.style.display =
            row.innerText.includes(month)
            ? ""
            : "none";

    });

}


// ==========================================
// Print Salary Slip
// ==========================================

function printSlip(id) {

    window.open(

        "/api/payroll/" + id,

        "_blank"

    );

}


// ==========================================
// Export PDF
// ==========================================

function exportPDF() {

    window.print();

}


// ==========================================
// Export Excel
// ==========================================

function exportExcel() {

    let csv = [];

    document
        .querySelectorAll("table tr")
        .forEach(row => {

            let data = [];

            row.querySelectorAll("th,td")
                .forEach(col => {

                    data.push(col.innerText);

                });

            csv.push(data.join(","));

        });

    const blob = new Blob(

        [csv.join("\n")],

        {

            type:"text/csv"

        }

    );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(blob);

    link.download =
        "Payroll_Report.csv";

    link.click();

}


// ==========================================
// Modal
// ==========================================

function openPayrollModal() {

    payrollId = null;

    document
        .getElementById("payrollModal")
        .style.display = "block";

}

function closePayrollModal() {

    document
        .getElementById("payrollModal")
        .style.display = "none";

    document
        .getElementById("payrollForm")
        .reset();

    document
        .getElementById("payrollForm")
        .onsubmit = savePayroll;

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}