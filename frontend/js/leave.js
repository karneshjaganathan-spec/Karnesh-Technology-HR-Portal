let leaveId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadLeaves();

    loadEmployees();

    document
        .getElementById("leaveForm")
        .addEventListener("submit", saveLeave);

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
// Load Leave Requests
// ==========================================

async function loadLeaves() {

    const response = await HRAPI.get("/leaves/");

    if (!response.success) {

        alert(response.message);
        return;

    }

    renderTable(response.data);

}


// ==========================================
// Render Table
// ==========================================

function renderTable(leaves) {

    const table = document.getElementById("leaveTable");

    table.innerHTML = "";

    if (leaves.length === 0) {

        table.innerHTML = `

            <tr>

                <td colspan="8" class="no-data">

                    No Leave Requests Found

                </td>

            </tr>

        `;

        return;

    }

    leaves.forEach(leave => {

        let badge = leave.status.toLowerCase();

        table.innerHTML += `

        <tr>

            <td>${leave.leave_id}</td>

            <td>${leave.employee_code} - ${leave.first_name} ${leave.last_name}</td>

            <td>${leave.leave_type}</td>

            <td>${leave.start_date}</td>

            <td>${leave.end_date}</td>

            <td>${leave.reason}</td>

            <td>

                <span class="badge ${badge}">

                    ${leave.status}

                </span>

            </td>

            <td>

                <button
                    class="action-btn edit-btn"
                    onclick="editLeave(${leave.leave_id})">

                    <i class="fa fa-edit"></i>

                </button>

                <button
                    class="action-btn approve-btn"
                    onclick="changeStatus(${leave.leave_id}, 'Approved')">

                    <i class="fa fa-check"></i>

                </button>

                <button
                    class="action-btn reject-btn"
                    onclick="changeStatus(${leave.leave_id}, 'Rejected')">

                    <i class="fa fa-times"></i>

                </button>

                <button
                    class="action-btn delete-btn"
                    onclick="deleteLeave(${leave.leave_id})">

                    <i class="fa fa-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

}


// ==========================================
// Load Employees
// ==========================================

async function loadEmployees() {

    const response = await HRAPI.get("/employees/");

    if (!response.success)
        return;

    const employee = document.getElementById("employee_id");

    employee.innerHTML = "";

    response.data.forEach(emp => {

        employee.innerHTML += `

            <option value="${emp.employee_id}">

                ${emp.employee_code}
                -
                ${emp.first_name}
                ${emp.last_name}

            </option>

        `;

    });

}


// ==========================================
// Apply Leave
// ==========================================

async function saveLeave(event) {

    event.preventDefault();

    const leave = {

        employee_id:
            parseInt(document.getElementById("employee_id").value),

        leave_type:
            document.getElementById("leave_type").value,

        start_date:
            document.getElementById("start_date").value,

        end_date:
            document.getElementById("end_date").value,

        reason:
            document.getElementById("reason").value,

        status:
            document.getElementById("status").value,

        applied_on:
            new Date().toISOString().slice(0, 10)

    };

    const response = await HRAPI.post(

        "/leaves/",

        leave

    );

    if (response.success) {

        alert("Leave Applied Successfully.");

        closeLeaveModal();

        document.getElementById("leaveForm").reset();

        loadLeaves();

    }
    else {

        alert(response.message);

    }

}


// ==========================================
// Edit Leave
// ==========================================

async function editLeave(id) {

    leaveId = id;

    const response = await HRAPI.get("/leaves/" + id);

    if (!response.success) {

        alert(response.message);
        return;

    }

    const leave = response.data;

    document.getElementById("employee_id").value = leave.employee_id;
    document.getElementById("leave_type").value = leave.leave_type;
    document.getElementById("start_date").value = leave.start_date;
    document.getElementById("end_date").value = leave.end_date;
    document.getElementById("reason").value = leave.reason;
    document.getElementById("status").value = leave.status;

    openLeaveModal();

    document
        .getElementById("leaveForm")
        .onsubmit = updateLeave;

}


// ==========================================
// Update Leave
// ==========================================

async function updateLeave(event) {

    event.preventDefault();

    const leave = {

        employee_id:
            parseInt(document.getElementById("employee_id").value),

        leave_type:
            document.getElementById("leave_type").value,

        start_date:
            document.getElementById("start_date").value,

        end_date:
            document.getElementById("end_date").value,

        reason:
            document.getElementById("reason").value,

        status:
            document.getElementById("status").value

    };

    const response = await HRAPI.put(

        "/leaves/" + leaveId,

        leave

    );

    if (response.success) {

        alert("Leave Updated Successfully.");

        closeLeaveModal();

        loadLeaves();

    }
    else {

        alert(response.message);

    }

}


// ==========================================
// Delete Leave
// ==========================================

async function deleteLeave(id) {

    if (!confirm("Delete this leave request?"))
        return;

    const response = await HRAPI.delete(

        "/leaves/" + id

    );

    if (response.success) {

        alert("Leave Deleted.");

        loadLeaves();

    }

}


// ==========================================
// Approve / Reject
// ==========================================

async function changeStatus(id, status) {

    const response = await HRAPI.put(

        "/leaves/" + id + "/status",

        {
            status: status
        }

    );

    if (response.success) {

        loadLeaves();

    }

}


// ==========================================
// Search Leave
// ==========================================

async function searchLeave() {

    const status = document
        .getElementById("statusFilter")
        .value;

    if (status === "") {

        loadLeaves();
        return;

    }

    const response = await HRAPI.get(

        "/leaves/search?status=" + status

    );

    if (response.success) {

        renderTable(response.data);

    }

}


// ==========================================
// Modal
// ==========================================

function openLeaveModal() {

    leaveId = null;

    document
        .getElementById("leaveModal")
        .style.display = "block";

}

function closeLeaveModal() {

    document
        .getElementById("leaveModal")
        .style.display = "none";

    document.getElementById("leaveForm").reset();

    document
        .getElementById("leaveForm")
        .onsubmit = saveLeave;

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}