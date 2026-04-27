import json
import socket

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ScanResult


class ScanConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        print("✅ WebSocket Connected")

    async def receive(self, text_data):
        print("🔥 Scan Started")

        data = json.loads(text_data)

        target = data.get("target")
        start_port = int(data.get("start_port", 1))
        end_port = int(data.get("end_port", 100))
        scan_type = data.get("scan_type", "custom")

        try:
            ip = socket.gethostbyname(target)
        except:
            await self.send(json.dumps({
                "log": "Invalid target"
            }))
            return

        # Scan Modes
        if scan_type == "quick":
            ports = range(1, 101)

        elif scan_type == "full":
            ports = range(1, 1000)

        elif scan_type == "stealth":
            ports = range(start_port, end_port + 1)

        else:
            ports = range(start_port, end_port + 1)

        for port in ports:
            await self.send(json.dumps({
                "log": f"Scanning port {port}"
            }))

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)

                result = sock.connect_ex((ip, port))

                if result == 0:
                    service = self.get_service(port)

                    # Save using async-safe DB call
                    user = self.scope["user"]

                    if user.is_authenticated:
                        await self.save_scan_result(
                            user,
                            target,
                            port,
                            service
                        )

                    await self.send(json.dumps({
                        "status": "OPEN",
                        "port": port,
                        "service": service
                    }))

                sock.close()

            except Exception as e:
                await self.send(json.dumps({
                    "log": f"Error on port {port}: {str(e)}"
                }))

        await self.send(json.dumps({
            "os": self.detect_os(ip)
        }))

    @database_sync_to_async
    def save_scan_result(self, user, target, port, service):
        ScanResult.objects.create(
            user=user,
            target=target,
            port=port,
            service=service,
            status="OPEN"
        )

    def get_service(self, port):
        common_ports = {
            20: "ftp-data",
            21: "ftp",
            22: "ssh",
            23: "telnet",
            25: "smtp",
            53: "dns",
            80: "http",
            110: "pop3",
            143: "imap",
            443: "https",
            3306: "mysql",
            3389: "rdp",
            5432: "postgresql",
            8080: "http-alt",
        }

        return common_ports.get(port, "Unknown")

    def detect_os(self, ip):
        return "Linux/Unix"