let permissions = [];

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadPermissions();

    document
        .getElementById("roleSelect")
        .addEventListener("change", loadRolePermissions);

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
// Load All Permissions
// ==========================================

async function loadPermissions() {

    const response = await HRAPI.get("/permissions/");

    if (!response.success)
        return;

    permissions = response.data;

    renderPermissions([]);

}


// ==========================================
// Render Permissions
// ==========================================

function renderPermissions(rolePermissions) {

    const table = document.getElementById("permissionTable");

    table.innerHTML = "";

    permissions.forEach(permission => {

        const checked =
            rolePermissions.includes(permission.permission_id)
            ? "checked"
            : "";

        table.innerHTML += `

        <tr>

            <td>

                <input

                    type="checkbox"

                    class="permission-checkbox"

                    value="${permission.permission_id}"

                    ${checked}

                >

            </td>

            <td>${permission.module_name}</td>

            <td>${permission.permission_name}</td>

            <td>${permission.description}</td>

        </tr>

        `;

    });

}


// ==========================================
// Load Role Permissions
// ==========================================

async function loadRolePermissions() {

    const roleId =
        document.getElementById("roleSelect").value;

    const response =
        await HRAPI.get(

            "/permissions/role/" + roleId

        );

    if (!response.success)
        return;

    renderPermissions(response.permissions);

}


// ==========================================
// Save Permissions
// ==========================================

async function savePermissions() {

    const roleId =
        document.getElementById("roleSelect").value;

    const permissionIds = [];

    document
        .querySelectorAll(".permission-checkbox")
        .forEach(box => {

            if (box.checked) {

                permissionIds.push(

                    Number(box.value)

                );

            }

        });

    const response =

        await HRAPI.put(

            "/permissions/role/" + roleId,

            {

                permission_ids: permissionIds

            }

        );

    if (response.success) {

        alert("Permissions Updated Successfully.");

    }

}


// ==========================================
// Search Permission
// ==========================================

function searchPermission() {

    const keyword =

        document

        .getElementById("searchPermission")

        .value

        .toLowerCase();

    document

        .querySelectorAll("#permissionTable tr")

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
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}