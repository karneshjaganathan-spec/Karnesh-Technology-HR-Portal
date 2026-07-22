document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadDashboard();

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
// Dashboard
// ==========================================

async function loadDashboard() {

    // Dashboard Cards
    const response = await HRAPI.get("/dashboard/stats");

    if (response.success) {

        document.getElementById("totalEmployees").innerText =
            response.data.total_employees;

        document.getElementById("activeEmployees").innerText =
            response.data.active_employees;

        document.getElementById("departments").innerText =
            response.data.total_departments;

        document.getElementById("attendanceToday").innerText =
            response.data.today_attendance;

        document.getElementById("pendingLeaves").innerText =
            response.data.pending_leaves;
    }

    // Load Tables
    loadRecentEmployees();
    loadDepartmentSummary();

    // Charts
    loadDepartmentChart();
    loadAttendanceChart();
    loadLeaveChart();
    loadPayrollChart();
}
async function loadRecentEmployees() {

    const response = await HRAPI.get("/dashboard/recent-employees");

    const table = document.getElementById("recentEmployees");

    table.innerHTML = "";

    if (!response.success) return;

    response.data.forEach(emp => {

        table.innerHTML += `
        <tr>
            <td>${emp.employee_code}</td>
            <td>${emp.first_name} ${emp.last_name}</td>
            <td>${emp.designation}</td>
            <td>${emp.joining_date}</td>
            <td>${emp.status}</td>
        </tr>
        `;
    });
}
async function loadDepartmentSummary() {

    const response = await HRAPI.get("/dashboard/departments");

    const table = document.getElementById("departmentSummary");

    table.innerHTML = "";

    if (!response.success) return;

    response.data.forEach(dept => {

        table.innerHTML += `
        <tr>
            <td>${dept.department_name}</td>
            <td>${dept.employee_count}</td>
        </tr>
        `;
    });
}


// ==========================================
// Department Pie Chart
// ==========================================

function loadDepartmentChart(){

    const ctx =
        document
        .getElementById("departmentChart");

    new Chart(ctx,{

        type:"pie",

        data:{

            labels:[

                "HR",

                "IT",

                "Finance",

                "Sales",

                "Admin"

            ],

            datasets:[{

                data:[

                    12,

                    28,

                    8,

                    18,

                    10

                ]

            }]

        },

        options:{

    responsive:true,

    maintainAspectRatio:false,

    layout:{
        padding:20
    },

    plugins:{
        legend:{
            position:"bottom",
            labels:{
                boxWidth:18,
                padding:20,
                font:{
                    size:14
                }
            }
        }
    }

}

    });

}


// ==========================================
// Attendance
// ==========================================

function loadAttendanceChart(){

    const ctx =

        document

        .getElementById("attendanceChart");

    new Chart(ctx,{

        type:"line",

        data:{

            labels:[

                "Jan",

                "Feb",

                "Mar",

                "Apr",

                "May",

                "Jun"

            ],

            datasets:[{

                label:"Attendance %",

                data:[

                    92,

                    95,

                    94,

                    96,

                    91,

                    97

                ],

                fill:false,

                tension:.3

            }]

        },

        options:{

            responsive:true

        }

    });

}


// ==========================================
// Leave
// ==========================================

function loadLeaveChart(){

    const ctx =

        document

        .getElementById("leaveChart");

    new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[

                "Approved",

                "Pending",

                "Rejected"

            ],

            datasets:[{

                data:[

                    30,

                    10,

                    5

                ]

            }]

        },

        options:{

    responsive:true,

    maintainAspectRatio:false,

    cutout:"50%",

    layout:{
        padding:20
    },

    plugins:{

        legend:{
            position:"top",

            labels:{
                boxWidth:18,
                padding:20,

                font:{
                    size:14
                }
            }
        },

        tooltip:{
            enabled:true
        }

    }

}

    });

}


// ==========================================
// Payroll
// ==========================================

function loadPayrollChart(){

    const ctx =

        document

        .getElementById("payrollChart");

    new Chart(ctx,{

        type:"bar",

        data:{

            labels:[

                "Jan",

                "Feb",

                "Mar",

                "Apr",

                "May",

                "Jun"

            ],

            datasets:[{

                label:"Payroll (₹ Lakhs)",

                data:[

                    5,

                    5.4,

                    5.3,

                    5.7,

                    5.6,

                    5.9

                ]

            }]

        },

        options:{

            responsive:true

        }

    });

}


// ==========================================
// Logout
// ==========================================

async function logout(){

    await HRAPI.post("/auth/logout",{});

    window.location.href="login.html";

}