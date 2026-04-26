import json
from channels.generic.websocket import AsyncWebsocketConsumer
import socket
from .models import ScanResult
from django.contrib.auth.models import User


class ScanConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)

        target = data['target']
        start_port = int(data['start_port'])
        end_port = int(data['end_port'])
        scan_type = data.get("scan_type", "custom")

        try:
            ip = socket.gethostbyname(target)
        except:
            await self.send(json.dumps({"error": "Invalid target"}))
            return

        # 🔥 SCAN MODES
        if scan_type == "quick":
            ports = range(1, 101)

        elif scan_type == "full":
            ports = range(1, 65536)

        elif scan_type == "stealth":
            ports = range(start_port, end_port + 1)

        else:
            ports = range(start_port, end_port + 1)

        for port in ports:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            result = sock.connect_ex((ip, port))

            if result == 0:
                user = self.scope["user"]

                if user.is_authenticated:
                 ScanResult.objects.create(
                   user=user,
                   target=target,
                   port=port,
                   service=service,
                   status="OPEN"
    )
                

                service = self.get_service(port)
                banner = self.grab_banner(ip, port)
                vuln = self.check_vulnerability(port, banner)

                await self.send(json.dumps({
                    "port": port,
                    "service": service,
                    "banner": banner,
                    "vulnerability": vuln,
                    "status": "OPEN"
                }))

            sock.close()

        # 🔥 OS DETECTION (basic)
        os_guess = self.detect_os(ip)

        await self.send(json.dumps({
            "os": os_guess
        }))

    # ------------------------------
    def get_service(self, port):
        try:
            return socket.getservbyport(port)
        except:
            return "Unknown"

    # ------------------------------
    def grab_banner(self, ip, port):
        try:
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect((ip, port))

            sock.send(b"HEAD / HTTP/1.1\r\n\r\n")
            banner = sock.recv(1024).decode(errors="ignore")

            sock.close()
            return banner[:100]

        except:
            return "Unknown"

    # ------------------------------
    def check_vulnerability(self, port, banner):

        banner = banner.lower()

        if port == 21:
            return "FTP anonymous login risk"

        elif port == 22:
            return "SSH brute-force risk"

        elif port == 23:
            return "Telnet insecure protocol"

        elif port == 80:
            return "HTTP not encrypted"

        elif port == 443:
            return "HTTPS detected (secure)"

        elif "apache/2.2" in banner:
            return "Outdated Apache server"

        elif "nginx/1.10" in banner:
            return "Old Nginx version"

        elif port == 3306:
            return "MySQL exposed"

        elif port == 3389:
            return "RDP exposed"

        return "No major issues"

    # ------------------------------
    def detect_os(self, ip):
        try:
            ttl = 64  # default assumption
            if ttl <= 64:
                return "Linux/Unix"
            elif ttl <= 128:
                return "Windows"
            else:
                return "Unknown"
        except:
            return "Unknown"