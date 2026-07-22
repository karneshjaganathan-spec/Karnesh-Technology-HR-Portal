let departmentChart = null;
let leaveChart = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadDashboard();

    loadDepartmentReport();

    loadAttendanceReport();

    loadLeaveReport();

    loadSalaryReport();

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
// Dashboard Summary
// ==========================================

async function loadDashboard() {

    const response = await HRAPI.get("/reports/dashboard");

    if (!response.success) return;

    const data = response.data;

    document.getElementById("employeesCount").innerText =
        data.employees;

    document.getElementById("departmentsCount").innerText =
        data.departments;

    document.getElementById("attendanceCount").innerText =
        data.attendance;

    document.getElementById("pendingLeaveCount").innerText =
        data.pending_leaves;

}


// ==========================================
// Department Report
// ==========================================

async function loadDepartmentReport() {

    const response = await HRAPI.get("/reports/departments");

    if (!response.success) return;

    const table = document.getElementById("departmentReport");

    table.innerHTML = "";

    let labels = [];
    let values = [];

    response.data.forEach(item => {

        labels.push(item.department_name);

        values.push(item.employee_count);

        table.innerHTML += `

        <tr>

            <td>${item.department_name}</td>

            <td>${item.employee_count}</td>

        </tr>

        `;

    });

    renderDepartmentChart(labels, values);

}


// ==========================================
// Attendance Report
// ==========================================

async function loadAttendanceReport() {

    const response = await HRAPI.get("/reports/attendance");

    if (!response.success) return;

    const table = document.getElementById("attendanceReport");

    table.innerHTML = "";

    response.data.forEach(item => {

        table.innerHTML += `

        <tr>

            <td>${item.attendance_date}</td>

            <td>${item.total}</td>

        </tr>

        `;

    });

}


// ==========================================
// Leave Report
// ==========================================

async function loadLeaveReport() {

    const response = await HRAPI.get("/reports/leaves");

    if (!response.success) return;

    const table = document.getElementById("leaveReport");

    table.innerHTML = "";

    let labels = [];
    let values = [];

    response.data.forEach(item => {

        labels.push(item.status);

        values.push(item.total);

        table.innerHTML += `

        <tr>

            <td>${item.status}</td>

            <td>${item.total}</td>

        </tr>

        `;

    });

    renderLeaveChart(labels, values);

}


// ==========================================
// Salary Report
// ==========================================

async function loadSalaryReport() {

    const response = await HRAPI.get("/reports/salary");

    if (!response.success) return;

    const table = document.getElementById("salaryReport");

    table.innerHTML = "";

    response.data.forEach(item => {

        table.innerHTML += `

        <tr>

            <td>${item.first_name} ${item.last_name}</td>

            <td>${item.designation}</td>

            <td>₹ ${Number(item.salary).toLocaleString()}</td>

        </tr>

        `;

    });

}


// ==========================================
// Department Chart
// ==========================================

function renderDepartmentChart(labels, values) {

    const ctx = document
        .getElementById("departmentChart")
        .getContext("2d");

    if (departmentChart) {
        departmentChart.destroy();
    }

    departmentChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{

                label: "Employees",

                data: values,

                backgroundColor: [
                    "#4f46e5",
                    "#2563eb",
                    "#0ea5e9",
                    "#06b6d4",
                    "#14b8a6"
                ],

                borderColor: "#1e3a8a",
                borderWidth: 1.5,
                borderRadius: 12,
                borderSkipped: false,

                hoverBackgroundColor: [
                    "#4338ca",
                    "#1d4ed8",
                    "#0284c7",
                    "#0891b2",
                    "#0f766e"
                ]

            }]

        },

        options: {

            responsive: true,
            maintainAspectRatio: false,

            animation: {
                duration: 800
            },

            interaction: {
                mode: "nearest",
                intersect: true
            },

            plugins: {

                legend: {
                    display: true,
                    position: "top",
                    labels: {
                        usePointStyle: true,
                        pointStyle: "circle",
                        padding: 20
                    }
                },

                tooltip: {
                    enabled: true,
                    backgroundColor: "#1f2937",
                    titleColor: "#fff",
                    bodyColor: "#fff",
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false
                }

            },

            scales: {

                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                },

                x: {
                    grid: {
                        display: false
                    }
                }

            }

        }

    });

}


// ==========================================
// Leave Chart
// ==========================================

function renderLeaveChart(labels, values) {

    const ctx = document
        .getElementById("leaveChart")
        .getContext("2d");

    if (leaveChart) {

        leaveChart.destroy();

    }

    leaveChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: labels,

            datasets: [

                {

                    data: values,

                    backgroundColor: [
                        "#28a745",
                        "#ffc107",
                        "#dc3545"
]

                }

            ]

        },

        options: {

    responsive: true,
    maintainAspectRatio: false,

    cutout: "60%",

    animation: {
        duration: 800
    },

    interaction: {
        mode: "nearest",
        intersect: true
    },

    plugins: {

        legend: {
            position: "top",
            labels: {
                usePointStyle: true,
                pointStyle: "circle",
                padding: 20
            }
        },

        tooltip: {
            enabled: true,
            backgroundColor: "#1f2937",
            titleColor: "#fff",
            bodyColor: "#fff",
            padding: 12,
            cornerRadius: 8
        }

    }

}

    });

}


// ==========================================
// Export PDF
// ==========================================

function exportPDF() {

    window.print();

}


// ==========================================
// Export Excel (CSV)
// ==========================================

function exportExcel() {

    let csv = [];

    const rows = document.querySelectorAll("table tr");

    rows.forEach(row => {

        let cols = row.querySelectorAll("td, th");

        let data = [];

        cols.forEach(col => {

            data.push(col.innerText);

        });

        csv.push(data.join(","));

    });

    const blob = new Blob(

        [csv.join("\n")],

        { type: "text/csv" }

    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "HR_Report.csv";

    a.click();

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}