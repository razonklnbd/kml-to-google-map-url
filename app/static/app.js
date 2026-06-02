function copyURL() {
    navigator.clipboard.writeText(
        document.getElementById("mapUrl").innerText
    );
}

function copyCSV() {
    let rows = document.querySelectorAll("table tr");
    let csv = [];

    rows.forEach(r => {
        let cols = r.querySelectorAll("td,th");
        csv.push([...cols].map(c => c.innerText).join(","));
    });

    navigator.clipboard.writeText(csv.join("\n"));
}