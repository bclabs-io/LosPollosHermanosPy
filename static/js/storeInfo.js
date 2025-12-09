const dropBtn = document.getElementById("dropBtn");
const content = document.getElementById("dropdown-content");
dropBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    content.style.display = content.style.display === "block" ? "none" : "block";
});
document.querySelectorAll("#dropdown-content input[type='checkbox']").forEach(checkbox => {
    checkbox.addEventListener("change", () => {
        const selected = [...document.querySelectorAll("#dropdown-content input[type='checkbox']")]
            .filter(c => c.checked)
            .map(c => c.value);
        if (selected.length === 0) {
            document.getElementById("dropBtn").textContent = "";
        } else {
            document.getElementById("dropBtn").textContent = selected.join(", ");
        }
    });
});