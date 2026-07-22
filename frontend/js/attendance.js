let attendanceId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadAttendance();

    loadEmployees();

    document
        .getElementById("attendanceForm")
        .addEventListener("submit", saveAttendance);

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
// Load Attendance
// ==========================================

async function loadAttendance() {

    const response = await HRAPI.get("/attendance/");

    if (!response.success) {

        alert(response.message);
        return;

    }

    renderAttendance(response.data);

}


// ==========================================
// Render Attendance Table
// ==========================================

function renderAttendance(records) {

    const table = document.getElementById("attendanceTable");

    table.innerHTML = "";

    if (records.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="8" class="no-data">
                    No Attendance Records Found
                </td>
            </tr>
        `;

        return;

    }

    records.forEach(record => {

        let badge = "";

        switch (record.status) {

            case "Present":
                badge = "present";
                break;

            case "Absent":
                badge = "absent";
                break;

            case "Leave":
                badge = "leave";
                break;

            default:
                badge = "half-day";
        }

        table.innerHTML += `

        <tr>

            <td>${record.attendance_id}</td>

            <td>${record.employee_code}</td>

            <td>${record.first_name} ${record.last_name}</td>

            <td>${record.attendance_date}</td>

            <td>${record.check_in}</td>

            <td>${record.check_out}</td>

            <td>

                <span class="badge ${badge}">

                    ${record.status}

                </span>

            </td>

            <td>

                <button
                    class="action-btn edit-btn"
                    onclick="editAttendance(${record.attendance_id})">

                    <i class="fa fa-edit"></i>

                </button>

                <button
                    class="action-btn delete-btn"
                    onclick="deleteAttendance(${record.attendance_id})">

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

                ${emp.employee_code} -
                ${emp.first_name}
                ${emp.last_name}

            </option>

        `;

    });

}


// ==========================================
// Save Attendance
// ==========================================

async function saveAttendance(event) {

    event.preventDefault();

    const attendance = {

        employee_id:
            parseInt(document.getElementById("employee_id").value),

        attendance_date:
            document.getElementById("attendance_date").value,

        check_in:
            document.getElementById("check_in").value,

        check_out:
            document.getElementById("check_out").value,

        status:
            document.getElementById("status").value

    };

    const response = await HRAPI.post(

        "/attendance/",

        attendance

    );

    if (response.success) {

        alert("Attendance Marked Successfully.");

        closeAttendanceModal();

        document.getElementById("attendanceForm").reset();

        loadAttendance();

    }
    else {

        alert(response.message);

    }

}


// ==========================================
// Search Attendance
// ==========================================

async function searchAttendance() {

    const date = document
        .getElementById("attendanceDate")
        .value;

    if (date === "") {

        loadAttendance();
        return;

    }

    const response = await HRAPI.get(

        "/attendance/search?date=" + date

    );

    if (!response.success)
        return;

    renderAttendance(response.data);

}


// ==========================================
// Delete Attendance
// ==========================================

async function deleteAttendance(id) {

    const ok = confirm(

        "Delete this attendance record?"

    );

    if (!ok)
        return;

    const response = await HRAPI.delete(

        "/attendance/" + id

    );

    if (response.success) {

        alert("Attendance Deleted.");

        loadAttendance();

    }
    else {

        alert(response.message);

    }

}


// ==========================================
// Edit Attendance
// ==========================================

async function editAttendance(id) {

    attendanceId = id;

    const response = await HRAPI.get(

        "/attendance/" + id

    );

    if (!response.success) {

        alert(response.message);
        return;

    }

    const attendance = response.data;

    document.getElementById("employee_id").value =
        attendance.employee_id;

    document.getElementById("attendance_date").value =
        attendance.attendance_date;

    document.getElementById("check_in").value =
        attendance.check_in;

    document.getElementById("check_out").value =
        attendance.check_out;

    document.getElementById("status").value =
        attendance.status;

    openAttendanceModal();

    document
        .getElementById("attendanceForm")
        .onsubmit = updateAttendance;

}


// ==========================================
// Update Attendance
// ==========================================

async function updateAttendance(event) {

    event.preventDefault();

    const attendance = {

        employee_id:
            parseInt(document.getElementById("employee_id").value),

        attendance_date:
            document.getElementById("attendance_date").value,

        check_in:
            document.getElementById("check_in").value,

        check_out:
            document.getElementById("check_out").value,

        status:
            document.getElementById("status").value

    };

    const response = await HRAPI.put(

        "/attendance/" + attendanceId,

        attendance

    );

    if (response.success) {

        alert("Attendance Updated Successfully.");

        closeAttendanceModal();

        document.getElementById("attendanceForm").reset();

        loadAttendance();

        document
            .getElementById("attendanceForm")
            .onsubmit = saveAttendance;

    }
    else {

        alert(response.message);

    }

}


// ==========================================
// Modal
// ==========================================

function openAttendanceModal() {

    attendanceId = null;

    document
        .getElementById("attendanceModal")
        .style.display = "block";

}

function closeAttendanceModal() {

    document
        .getElementById("attendanceModal")
        .style.display = "none";

    document.getElementById("attendanceForm").reset();

    document
        .getElementById("attendanceForm")
        .onsubmit = saveAttendance;

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