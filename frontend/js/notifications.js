let notificationId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadNotifications();

    document
        .getElementById("notificationForm")
        .addEventListener("submit", saveNotification);

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
// Load Notifications
// ==========================================

async function loadNotifications() {

    const response = await HRAPI.get("/notifications/");

    if (!response.success)
        return;

    const table =
        document.getElementById("notificationTable");

    table.innerHTML = "";

    let unread = 0;
    let today = 0;

    const currentDate =
        new Date().toISOString().split("T")[0];

    document.getElementById("totalNotifications").innerText =
        response.count;

    response.data.forEach(notification => {

        if (notification.is_read === 0)
            unread++;

        if (notification.created_at.startsWith(currentDate))
            today++;

        const badge =
            notification.is_read === 1
            ? "read"
            : "unread";

        const status =
            notification.is_read === 1
            ? "Read"
            : "Unread";

        table.innerHTML += `

        <tr>

            <td>${notification.notification_id}</td>

            <td>${notification.title}</td>

            <td>${notification.notification_type}</td>

            <td>${notification.recipient_type}</td>

            <td>

                <span class="badge ${badge}">

                    ${status}

                </span>

            </td>

            <td>

                ${notification.created_at}

            </td>

            <td>

                <button

                    class="action-btn read-btn"

                    onclick="markRead(${notification.notification_id})">

                    <i class="fa fa-check"></i>

                </button>

                <button

                    class="action-btn delete-btn"

                    onclick="deleteNotification(${notification.notification_id})">

                    <i class="fa fa-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

    document.getElementById("unreadNotifications").innerText =
        unread;

    document.getElementById("todayNotifications").innerText =
        today;

}


// ==========================================
// Save Notification
// ==========================================

async function saveNotification(event) {

    event.preventDefault();

    const notification = {

        title:
            document.getElementById("title").value,

        message:
            document.getElementById("message").value,

        notification_type:
            document.getElementById("notification_type").value,

        recipient_type:
            document.getElementById("recipient_type").value,

        recipient_id: null

    };

    const response =
        await HRAPI.post(

            "/notifications/",

            notification

        );

    if (response.success) {

        alert("Notification Created Successfully.");

        closeNotificationModal();

        document
            .getElementById("notificationForm")
            .reset();

        loadNotifications();

    }

    else {

        alert(response.message);

    }

}


// ==========================================
// Mark Read
// ==========================================

async function markRead(id) {

    const response =
        await HRAPI.put(

            "/notifications/" + id + "/read",

            {}

        );

    if (response.success) {

        loadNotifications();

    }

}


// ==========================================
// Delete
// ==========================================

async function deleteNotification(id) {

    if (!confirm("Delete notification?"))
        return;

    const response =
        await HRAPI.delete(

            "/notifications/" + id

        );

    if (response.success) {

        loadNotifications();

    }

}


// ==========================================
// Search
// ==========================================

function searchNotification() {

    const keyword =
        document
        .getElementById("searchNotification")
        .value
        .toLowerCase();

    document
        .querySelectorAll("#notificationTable tr")
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

function openNotificationModal() {

    notificationId = null;

    document
        .getElementById("notificationModal")
        .style.display = "block";

}

function closeNotificationModal() {

    document
        .getElementById("notificationModal")
        .style.display = "none";

    document
        .getElementById("notificationForm")
        .reset();

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}