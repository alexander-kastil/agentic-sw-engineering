async function api(path, options = {}) {
    const response = await fetch(path, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (response.status === 401 && !location.pathname.endsWith("/index.html") && location.pathname !== "/") {
        location.href = "/index.html";
        throw new Error("Not authenticated");
    }
    if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.detail || `Request failed with ${response.status}`);
    }
    return response.json();
}

const STATUS_LABELS = {
    Processing: ["Processing", "bg-secondary"],
    Shipped: ["Shipped", "bg-primary"],
    Delivered: ["Delivered", "bg-success"],
    PartialReturn: ["Partial Return", "bg-warning text-dark"],
    Returned: ["Returned", "bg-danger"],
};

function statusBadge(status) {
    const [label, css] = STATUS_LABELS[status] || [status, "bg-light text-dark"];
    return `<span class="badge ${css}">${label}</span>`;
}

function money(value) {
    return `$${Number(value).toFixed(2)}`;
}

function formatDate(value) {
    return value ? new Date(`${value.substring(0, 10)}T00:00:00`).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" }) : "";
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
}

async function renderNav() {
    const user = await api("/api/auth/me");
    document.getElementById("nav").innerHTML = `
        <nav class="navbar navbar-expand navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/orders.html">ContosoShop Support Portal</a>
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link" href="/orders.html">My Orders</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inventory.html">View Inventory</a></li>
                    <li class="nav-item"><a class="nav-link" href="/support.html">Contact Support</a></li>
                </ul>
                <span class="navbar-text me-3">${escapeHtml(user.name)}</span>
                <button class="btn btn-outline-light btn-sm" id="logout">Logout</button>
            </div>
        </nav>`;
    document.getElementById("logout").addEventListener("click", async () => {
        await api("/api/auth/logout", { method: "POST" });
        location.href = "/index.html";
    });
    return user;
}
