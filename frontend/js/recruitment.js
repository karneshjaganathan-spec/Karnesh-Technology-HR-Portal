let jobId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadJobs();

    loadCandidates();

    loadDepartments();

    document
        .getElementById("jobForm")
        .addEventListener("submit", saveJob);

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
// Load Jobs
// ==========================================

async function loadJobs() {

    const response = await HRAPI.get("/recruitment/jobs");

    if (!response.success)
        return;

    const table = document.getElementById("jobTable");

    table.innerHTML = "";

    document.getElementById("jobCount").innerText =
        response.count;

    response.data.forEach(job => {

        const badge =
            job.status.toLowerCase();

        table.innerHTML += `

        <tr>

            <td>${job.job_id}</td>

            <td>${job.job_title}</td>

            <td>${job.department}</td>

            <td>${job.vacancies}</td>

            <td>${job.experience}</td>

            <td>

                <span class="badge ${badge}">

                    ${job.status}

                </span>

            </td>

            <td>

                <button
                    class="action-btn edit-btn"
                    onclick="editJob(${job.job_id})">

                    <i class="fa fa-edit"></i>

                </button>

                <button
                    class="action-btn delete-btn"
                    onclick="deleteJob(${job.job_id})">

                    <i class="fa fa-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

}


// ==========================================
// Load Candidates
// ==========================================

async function loadCandidates() {

    const response =
        await HRAPI.get("/recruitment/candidates");

    if (!response.success)
        return;

    document.getElementById("candidateCount").innerText =
        response.count;

    const table =
        document.getElementById("candidateTable");

    table.innerHTML = "";

    response.data.forEach(candidate => {

        table.innerHTML += `

        <tr>

            <td>${candidate.candidate_id}</td>

            <td>

                ${candidate.first_name}

                ${candidate.last_name}

            </td>

            <td>${candidate.job_title}</td>

            <td>${candidate.email}</td>

            <td>${candidate.phone}</td>

            <td>

                <span class="badge ${candidate.status.toLowerCase()}">

                    ${candidate.status}

                </span>

            </td>

            <td>

                <select

                    onchange="updateStatus(

                        ${candidate.candidate_id},

                        this.value

                    )">

                    <option

                        ${candidate.status==="Applied"?"selected":""}>

                        Applied

                    </option>

                    <option

                        ${candidate.status==="Shortlisted"?"selected":""}>

                        Shortlisted

                    </option>

                    <option

                        ${candidate.status==="Selected"?"selected":""}>

                        Selected

                    </option>

                    <option

                        ${candidate.status==="Rejected"?"selected":""}>

                        Rejected

                    </option>

                </select>

            </td>

        </tr>

        `;

    });

}


// ==========================================
// Departments
// ==========================================

async function loadDepartments() {

    const response =
        await HRAPI.get("/departments/");

    if (!response.success)
        return;

    const department =
        document.getElementById("department");

    department.innerHTML = "";

    response.data.forEach(dep => {

        department.innerHTML += `

            <option value="${dep.department_name}">

                ${dep.department_name}

            </option>

        `;

    });

}


// ==========================================
// Save Job
// ==========================================

async function saveJob(event) {

    event.preventDefault();

    const job = {

        job_title:
            document.getElementById("job_title").value,

        department:
            document.getElementById("department").value,

        vacancies:
            Number(document.getElementById("vacancies").value),

        experience:
            document.getElementById("experience").value,

        location:
            document.getElementById("location").value,

        description:
            document.getElementById("description").value,

        status:
            document.getElementById("status").value

    };

    const response =
        await HRAPI.post(

            "/recruitment/jobs",

            job

        );

    if (response.success) {

        alert("Job Created Successfully.");

        closeJobModal();

        loadJobs();

    }

}


// ==========================================
// Edit Job
// ==========================================

async function editJob(id) {

    jobId = id;

    const response =
        await HRAPI.get(

            "/recruitment/jobs/" + id

        );

    if (!response.success)
        return;

    const job = response.data;

    document.getElementById("job_title").value =
        job.job_title;

    document.getElementById("department").value =
        job.department;

    document.getElementById("vacancies").value =
        job.vacancies;

    document.getElementById("experience").value =
        job.experience;

    document.getElementById("location").value =
        job.location;

    document.getElementById("description").value =
        job.description;

    document.getElementById("status").value =
        job.status;

    openJobModal();

    document
        .getElementById("jobForm")
        .onsubmit = updateJob;

}


// ==========================================
// Update Job
// ==========================================

async function updateJob(event) {

    event.preventDefault();

    const job = {

        job_title:
            document.getElementById("job_title").value,

        department:
            document.getElementById("department").value,

        vacancies:
            Number(document.getElementById("vacancies").value),

        experience:
            document.getElementById("experience").value,

        location:
            document.getElementById("location").value,

        description:
            document.getElementById("description").value,

        status:
            document.getElementById("status").value

    };

    const response =
        await HRAPI.put(

            "/recruitment/jobs/" + jobId,

            job

        );

    if (response.success) {

        alert("Job Updated.");

        closeJobModal();

        loadJobs();

    }

}


// ==========================================
// Delete Job
// ==========================================

async function deleteJob(id) {

    if (!confirm("Delete this Job?"))
        return;

    const response =
        await HRAPI.delete(

            "/recruitment/jobs/" + id

        );

    if (response.success) {

        loadJobs();

    }

}


// ==========================================
// Candidate Status
// ==========================================

async function updateStatus(id, status) {

    await HRAPI.put(

        "/recruitment/candidates/" +

        id +

        "/status",

        {

            status: status

        }

    );

    loadCandidates();

}


// ==========================================
// Search Job
// ==========================================

function searchJob() {

    const keyword =
        document
        .getElementById("searchJob")
        .value
        .toLowerCase();

    document
        .querySelectorAll("#jobTable tr")
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

function openJobModal() {

    jobId = null;

    document
        .getElementById("jobModal")
        .style.display = "block";

}

function closeJobModal() {

    document
        .getElementById("jobModal")
        .style.display = "none";

    document
        .getElementById("jobForm")
        .reset();

    document
        .getElementById("jobForm")
        .onsubmit = saveJob;

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}