<div align="center">

# Advanced Port Scanner & Network Recon Tool

Real-Time Cybersecurity Scanning System built using Django, WebSockets, and Python Sockets.

<img src="https://img.shields.io/badge/Django-5.0-green?style=flat-square&logo=django">
<img src="https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python">
<img src="https://img.shields.io/badge/WebSockets-Realtime-orange?style=flat-square">

</div>

---

## Overview

Advanced Port Scanner is a real-time network reconnaissance system designed for educational and cybersecurity research purposes.

The application performs:

- Live port scanning
- Banner grabbing
- Basic OS fingerprinting
- Vulnerability hint detection
- Real-time WebSocket communication

The project demonstrates practical implementation of networking and OSI layer concepts using Django and socket programming.

---

## Features

✔ Real-time live scanning  
✔ Quick / Full / Stealth scan modes  
✔ Banner grabbing  
✔ OS detection  
✔ Vulnerability hints  
✔ PDF report generation  
✔ User authentication  
✔ Scan history tracking  
✔ Hacker-style dark neon UI  
✔ Matrix rain animation  

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Django | Backend Framework |
| Django Channels | WebSocket Support |
| Daphne | ASGI Server |
| SQLite | Database |
| HTML/CSS/JavaScript | Frontend |
| Python Sockets | Network Scanning |

---

## Installation

Clone repository:

```bash
git clone https://github.com/yourusername/portscanner.git
cd portscanner
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run server:

```bash
daphne -b 127.0.0.1 -p 8000 portscanner.asgi:application
```

---

## Usage

1. Open browser:
   `http://127.0.0.1:8000`

2. Login to dashboard

3. Enter:
   - Target IP
   - Port range
   - Scan mode

4. Click:
   `EXECUTE`

5. Live scan results will appear instantly.

---

## Educational Objectives

This project demonstrates:

- TCP/IP communication
- Socket programming
- OSI model implementation
- Real-time WebSockets
- Service enumeration
- Basic cybersecurity reconnaissance

---

## Disclaimer

This project was developed strictly for educational and authorized security testing purposes only.

Unauthorized scanning of systems or networks without permission may violate cybersecurity laws.

---

## Author

Shivam  
Cybersecurity & Networking Enthusiast
