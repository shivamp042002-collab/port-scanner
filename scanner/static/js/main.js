let socket;

function startScan() {
    let target = document.getElementById("target").value;
    let start_port = document.getElementById("start_port").value;
    let end_port = document.getElementById("end_port").value;
    let scan_type = document.getElementById("scan_type").value;

    let consoleBox = document.getElementById("console");
    let progressBar = document.getElementById("bar");

    // Reset console + progress bar
    consoleBox.innerHTML = "> Initializing Cyber Scan...\n";
    progressBar.style.width = "0%";

    // Validation
    if (!target) {
        consoleBox.innerHTML += "> ERROR: Please enter target IP or Domain\n";
        return;
    }

    if (!start_port) start_port = 1;
    if (!end_port) end_port = 100;

    // Close old socket if already running
    if (socket) {
        socket.close();
    }

    // WebSocket Connection
    socket = new WebSocket("ws://127.0.0.1:8000/ws/scan/");

    socket.onopen = function () {
        console.log("✅ WebSocket Connected");

        consoleBox.innerHTML += "> Connection Established...\n";
        consoleBox.innerHTML += "> Starting Port Scan...\n\n";

        socket.send(JSON.stringify({
            target: target,
            start_port: start_port,
            end_port: end_port,
            scan_type: scan_type
        }));
    };

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);

        // Progress Bar Animation
        let currentWidth = parseInt(progressBar.style.width) || 0;
        if (currentWidth < 95) {
            progressBar.style.width = (currentWidth + 1) + "%";
        }

        // Logs
        if (data.log) {
            consoleBox.innerHTML += "> " + data.log + "\n";
        }

        // Open Port Detection
        if (data.status === "OPEN") {
            consoleBox.innerHTML +=
                "> OPEN PORT DETECTED → Port: " +
                data.port +
                " | Service: " +
                data.service +
                "\n";
        }

        // OS Detection
        if (data.os) {
            consoleBox.innerHTML +=
                "\n> TARGET OS DETECTED: " +
                data.os +
                "\n";

            consoleBox.innerHTML +=
                "\n> Scan Completed Successfully ✅\n";

            progressBar.style.width = "100%";
        }

        // Auto-scroll console
        consoleBox.scrollTop = consoleBox.scrollHeight;
    };

    socket.onerror = function () {
        consoleBox.innerHTML +=
            "\n> ERROR: WebSocket Connection Failed ❌\n";
    };

    socket.onclose = function () {
        consoleBox.innerHTML +=
            "\n> Connection Closed.\n";
    };
}