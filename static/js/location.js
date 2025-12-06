document.addEventListener("DOMContentLoaded", () => {
    addBlock();
});

async function addBlock() {
    const locoContainer = document.getElementById("loco");
    // const res = await fetch("/api/location/getAll");
    // if (!res.ok) {
    //     // Throw a meaningful error if the network request fails
    //     throw new Error(`HTTP error! status: ${res.status}`);
    // }
    // const locations = await res.json();
    const locations = []; // Temporary empty array for testing

    // If no locations are returned, exit the function
    if (locations.length === 0) {
        locoContainer.innerHTML = "<p>No locations found.</p>";
        return;
    }

    locations.forEach((location) => {
        const getDaysString = (loc) => {
            const daysMap = {
                mon: "Mon",
                tue: "Tue",
                wed: "Wed",
                thu: "Thu",
                fri: "Fri",
                sat: "Sat",
                sun: "Sun",
            };
            const activeDays = Object.entries(daysMap)
                // Check for a truthy value (1 in your database structure)
                .filter(([key]) => loc[key] === 1)
                .map(([, value]) => value);
            return activeDays.length > 0 ? activeDays.join(", ") : "Not opened to public";
        };

        const daysOpenString = getDaysString(location);
        locoContainer.innerHTML += `
                <div class="locoBlock" data-location-id="${location.sId}">
                    <p class="line"><strong>City:</strong> ${location.city}</p>
                    <p class="line"><strong>Address:</strong> ${location.address}, ${location.zipcode}</p>
                    <p class="line"><strong>Coordinates:</strong> ${location.latitude}, ${location.longitude}</p>
                    <p class="line"><strong>Open Days:</strong> ${daysOpenString}</p>
                    <p class="line"><strong>Hours:</strong> ${location.open_time} - ${location.close_time}</p>
                </div>
            `;
    });
}

document.getElementById("addLocationBtn").addEventListener("click", (e) => {
    document.getElementById("addLocoPlaceholder").classList.toggle("invisible");
});

const dropBtn = document.getElementById("dropBtn");
const content = document.getElementById("dropdown-content");

dropBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    content.style.display = content.style.display === "block" ? "none" : "block";
});

document.querySelectorAll("#dropdown-content input[type='checkbox']").forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
        const selected = [...document.querySelectorAll("#dropdown-content input[type='checkbox']")]
            .filter((c) => c.checked)
            .map((c) => c.value);
        if (selected.length === 0) {
            document.getElementById("dropBtn").textContent = "";
        } else {
            document.getElementById("dropBtn").textContent = selected.join(", ");
        }
    });
});

document.getElementById("submitLocoBtn").addEventListener("click", async (e) => {
    e.preventDefault();
    const form = document.getElementById("addLocoPlaceholder");
    const formData = new FormData(form);
    const checkboxes = document.querySelectorAll("#dropdown-content input[type='checkbox']");
    const daysBoolArray = Array.from(checkboxes).map((cb) => cb.checked);
    const data = {
        latitude: formData.get("latitude"),
        longitude: formData.get("longitude"),
        city: formData.get("city"),
        address: formData.get("address"),
        zipcode: formData.get("zip"),
        days: daysBoolArray,
        open_time: formData.get("open"),
        close_time: formData.get("close"),
    };
    alert("Sending...");
    const res = await fetch("/api/location/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await res.json();
    if (result.success) {
        alert("Location added successfully!");
        window.location.reload();
    }
});
