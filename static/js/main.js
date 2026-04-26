let socket;

function startScan() {

    let target = document.getElementById("target").value;
    let start = document.getElementById("start_port").value;
    let end = document.getElementById("end_port").value;
    let scan_type = document.getElementById("scan_type").value;

    let consoleBox = document.getElementById("console");
    let resultsDiv = document.getElementById("results");
    let bar = document.getElementById("bar");

    consoleBox.innerHTML = "> Connecting...\n";
    resultsDiv.innerHTML = "";
    bar.style.width = "0%";
    let protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

    socket = new WebSocket(protocol + window.location.host + "/ws/scan/");

    socket.onopen = function () {
        consoleBox.innerHTML += "> Connected\n";

        socket.send(JSON.stringify({
            target: target,
            start_port: start,
            end_port: end,
            scan_type: scan_type
        }));
    };

    socket.onmessage = function (event) {

        let data = JSON.parse(event.data);

        if (data.error) {
            consoleBox.innerHTML += "> ERROR: " + data.error + "\n";
            return;
        }

        if (data.port) {

            consoleBox.innerHTML += `> OPEN: ${data.port} (${data.service})\n`;
            consoleBox.innerHTML += `> Banner: ${data.banner}\n`;
            consoleBox.innerHTML += `> Vulnerability: ${data.vulnerability}\n\n`;

            let row = `<tr>
                <td>${data.port}</td>
                <td>${data.service}</td>
                <td>${data.banner}</td>
                <td>${data.vulnerability}</td>
            </tr>`;

            if (!resultsDiv.innerHTML) {
                resultsDiv.innerHTML =
                "<table><tr><th>PORT</th><th>SERVICE</th><th>BANNER</th><th>VULNERABILITY</th></tr></table>";
            }

            resultsDiv.querySelector("table").innerHTML += row;
        }

        if (data.os) {
            consoleBox.innerHTML += "> OS DETECTED: " + data.os + "\n";
        }
    };

    socket.onclose = function () {
        consoleBox.innerHTML += "> Scan Complete\n";
        bar.style.width = "100%";
    };
}