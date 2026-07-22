let assetId = null;

document.addEventListener("DOMContentLoaded", () => {

    checkLogin();

    loadSummary();

    loadAssets();

    loadEmployees();

    document
        .getElementById("assetForm")
        .addEventListener("submit", saveAsset);

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
// Load Dashboard Summary
// ==========================================

async function loadSummary() {

    const response = await HRAPI.get("/assets/summary");

    if (!response.success)
        return;

    const summary = response.data;

    document.getElementById("totalAssets").innerText =
        summary.total_assets || 0;

    document.getElementById("availableAssets").innerText =
        summary.available_assets || 0;

    document.getElementById("assignedAssets").innerText =
        summary.assigned_assets || 0;

    document.getElementById("maintenanceAssets").innerText =
        summary.maintenance_assets || 0;

}


// ==========================================
// Load Employees
// ==========================================

async function loadEmployees() {

    const response = await HRAPI.get("/employees/");

    if (!response.success)
        return;

    const employee =
        document.getElementById("employee_id");

    employee.innerHTML =
        `<option value="">Not Assigned</option>`;

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
// Load Assets
// ==========================================

async function loadAssets() {

    const response = await HRAPI.get("/assets/");

    if (!response.success)
        return;

    renderAssets(response.data);

}


// ==========================================
// Render Assets
// ==========================================

function renderAssets(assets) {

    const table =
        document.getElementById("assetTable");

    table.innerHTML = "";

    if (assets.length === 0) {

        table.innerHTML = `

        <tr>

            <td colspan="8">

                No Assets Found

            </td>

        </tr>

        `;

        return;

    }

    assets.forEach(asset => {

        let badge =
            asset.status.toLowerCase();

        table.innerHTML += `

        <tr>

            <td>${asset.asset_code}</td>

            <td>${asset.asset_name}</td>

            <td>${asset.category}</td>

            <td>${asset.brand || "-"}</td>

            <td>

                ${asset.employee_code || "-"}

            </td>

            <td>

                <span class="badge ${badge}">

                    ${asset.status}

                </span>

            </td>

            <td>

                ${asset.warranty_expiry || "-"}

            </td>

            <td>

                <button

                    class="action-btn edit-btn"

                    onclick="editAsset(${asset.asset_id})">

                    <i class="fa fa-edit"></i>

                </button>

                <button

                    class="action-btn delete-btn"

                    onclick="deleteAsset(${asset.asset_id})">

                    <i class="fa fa-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

}


// ==========================================
// Save Asset
// ==========================================

async function saveAsset(event) {

    event.preventDefault();

    const asset = {

        asset_code:
            document.getElementById("asset_code").value,

        asset_name:
            document.getElementById("asset_name").value,

        category:
            document.getElementById("category").value,

        brand:
            document.getElementById("brand").value,

        model:
            document.getElementById("model").value,

        serial_number:
            document.getElementById("serial_number").value,

        purchase_date:
            document.getElementById("purchase_date").value,

        purchase_cost:
            Number(document.getElementById("purchase_cost").value),

        warranty_expiry:
            document.getElementById("warranty_expiry").value,

        status:
            document.getElementById("status").value,

        employee_id:
            document.getElementById("employee_id").value || null,

        assigned_date:
            document.getElementById("assigned_date").value,

        remarks:
            document.getElementById("remarks").value

    };

    let response;

    if (assetId === null) {

        response = await HRAPI.post("/assets/", asset);

    } else {

        response = await HRAPI.put(

            "/assets/" + assetId,

            asset

        );

    }

    if (response.success) {

        alert(

            assetId === null

            ? "Asset Added Successfully."

            : "Asset Updated Successfully."

        );

        closeAssetModal();

        loadAssets();

        loadSummary();

    }

}


// ==========================================
// Edit Asset
// ==========================================

async function editAsset(id) {

    assetId = id;

    const response =
        await HRAPI.get("/assets/" + id);

    if (!response.success)
        return;

    const asset = response.data;

    document.getElementById("asset_code").value =
        asset.asset_code;

    document.getElementById("asset_name").value =
        asset.asset_name;

    document.getElementById("category").value =
        asset.category;

    document.getElementById("brand").value =
        asset.brand;

    document.getElementById("model").value =
        asset.model;

    document.getElementById("serial_number").value =
        asset.serial_number;

    document.getElementById("purchase_date").value =
        asset.purchase_date;

    document.getElementById("purchase_cost").value =
        asset.purchase_cost;

    document.getElementById("warranty_expiry").value =
        asset.warranty_expiry;

    document.getElementById("status").value =
        asset.status;

    document.getElementById("employee_id").value =
        asset.employee_id || "";

    document.getElementById("assigned_date").value =
        asset.assigned_date || "";

    document.getElementById("remarks").value =
        asset.remarks || "";

    openAssetModal();

}


// ==========================================
// Delete Asset
// ==========================================

async function deleteAsset(id) {

    if (!confirm("Delete this asset?"))
        return;

    const response =
        await HRAPI.delete("/assets/" + id);

    if (response.success) {

        loadAssets();

        loadSummary();

    }

}


// ==========================================
// Search & Filter
// ==========================================

function filterAssets() {

    const keyword =
        document.getElementById("searchAsset")
        .value
        .toLowerCase();

    const status =
        document.getElementById("statusFilter")
        .value
        .toLowerCase();

    document
        .querySelectorAll("#assetTable tr")
        .forEach(row => {

            const text =
                row.innerText.toLowerCase();

            const matchKeyword =
                text.includes(keyword);

            const matchStatus =
                status === "" ||
                text.includes(status);

            row.style.display =
                matchKeyword && matchStatus
                ? ""
                : "none";

        });

}


// ==========================================
// Modal
// ==========================================

function openAssetModal() {

    assetId = null;

    document
        .getElementById("assetModal")
        .style.display = "block";

}

function closeAssetModal() {

    document
        .getElementById("assetModal")
        .style.display = "none";

    document
        .getElementById("assetForm")
        .reset();

}


// ==========================================
// Logout
// ==========================================

async function logout() {

    await HRAPI.post("/auth/logout", {});

    window.location.href = "login.html";

}