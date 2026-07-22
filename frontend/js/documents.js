let currentUser = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadEmployees();

    loadDocuments();

    document
        .getElementById("documentForm")
        .addEventListener("submit", uploadDocument);

});


// ==========================================
// Check Login
// ==========================================

async function checkLogin() {

    const response = await HRAPI.get("/auth/me");

    if (!response.logged_in) {

        window.location.href = "login.html";
        return;

    }

    currentUser = response.user;

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
// Load Documents
// ==========================================

async function loadDocuments() {

    const response = await HRAPI.get("/documents/");

    if (!response.success)
        return;

    const table = document.getElementById("documentTable");

    table.innerHTML = "";

    let employees = new Set();

    let todayUploads = 0;

    const today = new Date().toISOString().split("T")[0];

    document.getElementById("totalDocuments").innerText =
        response.count;

    response.data.forEach(doc => {

        employees.add(doc.employee_id);

        if (doc.uploaded_on === today)
            todayUploads++;

        table.innerHTML += `

        <tr>

            <td>${doc.document_id}</td>

            <td>

                ${doc.employee_code}

                -

                ${doc.first_name}

                ${doc.last_name}

            </td>

            <td>${doc.document_name}</td>

            <td>${doc.document_type}</td>

            <td>${doc.uploaded_on}</td>

            <td>${doc.remarks || ""}</td>

            <td>

                <button

                    class="action-btn download-btn"

                    onclick="downloadDocument(${doc.document_id})">

                    <i class="fa fa-download"></i>

                </button>

                <button

                    class="action-btn delete-btn"

                    onclick="deleteDocument(${doc.document_id})">

                    <i class="fa fa-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

    document.getElementById("employeeDocuments").innerText =
        employees.size;

    document.getElementById("todayUploads").innerText =
        todayUploads;

}


// ==========================================
// Upload Document
// ==========================================

async function uploadDocument(event) {

    event.preventDefault();

    const formData = new FormData();

    formData.append(
        "employee_id",
        document.getElementById("employee_id").value
    );

    formData.append(
        "document_name",
        document.getElementById("document_name").value
    );

    formData.append(
        "document_type",
        document.getElementById("document_type").value
    );

    formData.append(
        "remarks",
        document.getElementById("remarks").value
    );

    formData.append(
        "uploaded_by",
        currentUser.id
    );

    formData.append(
        "file",
        document.getElementById("file").files[0]
    );

    const response = await fetch(

        `${HRAPI.baseURL}/documents/upload`,

        {

            method: "POST",

            body: formData,

            credentials: "include"

        }

    );

    const result = await response.json();

    if (result.success) {

        alert("Document Uploaded Successfully.");

        closeUploadModal();

        document.getElementById("documentForm").reset();

        loadDocuments();

    }

    else {

        alert(result.message);

    }

}


// ==========================================
// Download
// ==========================================

function downloadDocument(id) {

    window.open(

        `${HRAPI.baseURL}/documents/download/${id}`,

        "_blank"

    );

}


// ==========================================
// Delete
// ==========================================

async function deleteDocument(id) {

    if (!confirm("Delete this document?"))
        return;

    const response = await HRAPI.delete(

        "/documents/" + id

    );

    if (response.success) {

        loadDocuments();

    }

}


// ==========================================
// Search
// ==========================================

function searchDocument() {

    const keyword =

        document

        .getElementById("searchDocument")

        .value

        .toLowerCase();

    document

        .querySelectorAll("#documentTable tr")

        .forEach(row => {

            row.style.display =

                row.innerText

                    .toLowerCase()

                    .includes(keyword)

                ? ""

                : "none";

        });

}


// ==========================================
// Modal
// ==========================================

function openUploadModal() {

    document.getElementById("uploadModal").style.display =
        "block";

}

function closeUploadModal() {

    document.getElementById("uploadModal").style.display =
        "none";

    document.getElementById("documentForm").reset();

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}