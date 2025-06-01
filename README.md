# SIYI A8 Mini Gimbal + Drone Status Tools

This repository contains two integrated tools designed to enhance operation and monitoring of drones equipped with SIYI A8 mini gimbal cameras. It includes:

- **Gimbal Camera Control Utility** — Real-time pitch, yaw, zoom, and recording controls via command-line.
- **System Status Reporter** — Automated drone system diagnostics and email reports on boot, including camera stream status, device pings, and network metrics.

---

## 📦 Contents

- `A8miniControl.c` – Control interface for SIYI gimbals using UDP protocol.
- `report.py` – System monitoring script for capturing boot diagnostics and emailing status.
- `.env` – Configuration file for credentials, IPs, and telemetry settings.

---

## 🔧 Setup

1. **Install dependencies**:
   - Python 3 with `psutil`, `python-dotenv`
   - Tools: `ffmpeg`, `ffprobe`, `speedtest-cli`
   - `gcc` (for compiling camera control binary)

2. **Configure `.env`**:
   ```env
   EMAIL_SENDER=your@email.com
   EMAIL_PASSWORD=your_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_RECIPIENTS=person1@example.com,person2@example.com

   AIRCRAFT_NAME=SkyWhale
   SERIAL_NUMBER=SW123456
   FAA_REGISTRATION=REG123456
   TAIL_NUMBER=SW2401

   RESTREAM_URL=rtsp://192.168.193.100:8554/camera
   SIYI_RTSP=rtsp://192.168.144.25:8554/main.264

   AIR_DATA_TX_IP=192.168.144.11
   GROUND_STATION_IP=192.168.144.12
   SIYI_IP=192.168.144.25
   SIYI_AI_IP=192.168.144.60
