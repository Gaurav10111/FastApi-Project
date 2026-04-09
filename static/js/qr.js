document.getElementById("qrForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    const params = new URLSearchParams({
        name: formData.get("name"),
        date: formData.get("date"),
        start_time: formData.get("start_time"),
        end_time: formData.get("end_time")
    });

    const response = await fetch("/qr/create?" + params.toString(), {
        method: "POST",
        headers: getAuthHeaders()
    });

    const data = await response.json();

    if (data.detail === "Token expired") {
        alert("Session expired, login again");
        localStorage.removeItem("token");
        window.location.href = "/";
        return;
    }

    if (data.qr_image) {
        document.getElementById("result").innerHTML = `
            <p>${data.message}</p>
            <img src="${data.qr_image}" width="200"/>
            <p>${data.scan_url}</p>
        `;
    } else {
        document.getElementById("result").innerHTML = `<p>${data.detail}</p>`;
    }
});