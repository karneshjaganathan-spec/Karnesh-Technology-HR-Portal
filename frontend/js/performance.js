let reviewId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadReviews();

    loadEmployees();

    document
        .getElementById("reviewForm")
        .addEventListener("submit", saveReview);

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
// Load Reviews
// ==========================================

async function loadReviews() {

    const response = await HRAPI.get("/performance/");

    if (!response.success)
        return;

    const table =
        document.getElementById("reviewTable");

    table.innerHTML = "";

    let totalRating = 0;

    let promotions = 0;

    document.getElementById("reviewCount").innerText =
        response.count;

    response.data.forEach(review => {

        totalRating += Number(review.overall_rating);

        if (review.promotion_recommended === "Yes")
            promotions++;

        let badge = "poor";

        if (review.overall_rating >= 8)
            badge = "excellent";

        else if (review.overall_rating >= 6)
            badge = "good";

        else if (review.overall_rating >= 4)
            badge = "average";

        table.innerHTML += `

        <tr>

            <td>${review.review_id}</td>

            <td>

                ${review.employee_code}

                -

                ${review.first_name}

                ${review.last_name}

            </td>

            <td>${review.designation}</td>

            <td>${review.review_period}</td>

            <td>${review.reviewer_name}</td>

            <td>

                <span class="rating ${badge}">

                    ${review.overall_rating}

                </span>

            </td>

            <td>${review.status}</td>

            <td>

                <button

                    class="action-btn view-btn"

                    onclick="viewReview(${review.review_id})">

                    <i class="fa fa-eye"></i>

                </button>

                <button

                    class="action-btn delete-btn"

                    onclick="deleteReview(${review.review_id})">

                    <i class="fa fa-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

    document.getElementById("avgRating").innerText =

        response.count === 0

        ? "0"

        : (totalRating / response.count).toFixed(2);

    document.getElementById("promotionCount").innerText =
        promotions;

}


// ==========================================
// Employees
// ==========================================

async function loadEmployees() {

    const response =
        await HRAPI.get("/employees/");

    if (!response.success)
        return;

    const employee =
        document.getElementById("employee_id");

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
// Save Review
// ==========================================

async function saveReview(event) {

    event.preventDefault();

    const review = {

        employee_id:
            parseInt(document.getElementById("employee_id").value),

        review_period:
            document.getElementById("review_period").value,

        reviewer_name:
            document.getElementById("reviewer_name").value,

        kpi_score:
            Number(document.getElementById("kpi_score").value),

        attendance_score:
            Number(document.getElementById("attendance_score").value),

        teamwork_score:
            Number(document.getElementById("teamwork_score").value),

        communication_score:
            Number(document.getElementById("communication_score").value),

        strengths:
            document.getElementById("strengths").value,

        improvements:
            document.getElementById("improvements").value,

        manager_comments:
            document.getElementById("manager_comments").value,

        employee_comments:
            document.getElementById("employee_comments").value,

        promotion_recommended:
            document.getElementById("promotion_recommended").value,

        review_date:
            document.getElementById("review_date").value,

        status:
            document.getElementById("status").value

    };

    const response =
        await HRAPI.post("/performance/", review);

    if (response.success) {

        alert("Performance Review Saved.");

        closeReviewModal();

        document
            .getElementById("reviewForm")
            .reset();

        loadReviews();

    }

    else {

        alert(response.message);

    }

}


// ==========================================
// View Review
// ==========================================

async function viewReview(id) {

    const response =
        await HRAPI.get("/performance/" + id);

    if (!response.success)
        return;

    const review = response.data;

    alert(

`Employee Review

Reviewer : ${review.reviewer_name}

Overall Rating : ${review.overall_rating}

Strengths :

${review.strengths}

Improvements :

${review.improvements}

Manager Comments :

${review.manager_comments}

Employee Comments :

${review.employee_comments}`

    );

}


// ==========================================
// Delete Review
// ==========================================

async function deleteReview(id) {

    if (!confirm("Delete this review?"))
        return;

    const response =
        await HRAPI.delete("/performance/" + id);

    if (response.success) {

        loadReviews();

    }

}


// ==========================================
// Search
// ==========================================

function searchReview() {

    const keyword =
        document
        .getElementById("searchEmployee")
        .value
        .toLowerCase();

    document
        .querySelectorAll("#reviewTable tr")
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

function openReviewModal() {

    reviewId = null;

    document
        .getElementById("reviewModal")
        .style.display = "block";

}

function closeReviewModal() {

    document
        .getElementById("reviewModal")
        .style.display = "none";

    document
        .getElementById("reviewForm")
        .reset();

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}