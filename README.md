# 🛰️ SIYI A8 Mini Gimbal + Drone Status Tools

This repository contains integrated utilities to operate and monitor drones equipped with **SIYI A8 Mini gimbals**. It includes:

- 🎮 **Camera Control Utility** – Real-time command-line control of pitch, yaw, zoom, recording, and stream restart.
- 📡 **System Status Reporter** – Automatic diagnostics and email alerts sent on boot (connectivity, stream health, telemetry status).

---

## 📁 Contents

| File/Folder         | Description                                                  |
|---------------------|--------------------------------------------------------------|
| `A8miniControl.c`   | C source for SIYI A8 gimbal control via UDP commands         |
| `cam_ctrl.py`       | Python CLI tool for ergonomic gimbal control via numpad keys |
| `restartVideo.sh`   | Script to restart the SIYI RTSP stream                       |
| `report.py`         | Boot-time diagnostics, email reports, and stream checks      |
| `.env`              | Environment config for camera, telemetry, and email          |

---

## 🧰 Setup

### 1. Install System Dependencies

```bash
sudo apt update && sudo apt install -y \
    gcc ffmpeg ffprobe speedtest-cli \
    python3-pip

pip3 install psutil python-dotenv
2. Compile Gimbal Control Tool
bash
Copy
Edit
gcc -o A8miniControl A8miniControl.c
Ensure A8miniControl is in the same directory as cam_ctrl.py.

3. Configure .env File
env
Copy
Edit
# Email Settings
EMAIL_SENDER=you@example.com
EMAIL_PASSWORD=yourpassword
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_RECIPIENTS=admin1@example.com,admin2@example.com

# Aircraft Info
AIRCRAFT_NAME=SkyWhale
SERIAL_NUMBER=SW123456
FAA_REGISTRATION=REG123456
TAIL_NUMBER=SW2401

# Video and Network Info
RESTREAM_URL=rtsp://192.168.193.100:8554/camera
SIYI_RTSP=rtsp://192.168.144.25:8554/main.264

# Network Devices
AIR_DATA_TX_IP=192.168.144.11
GROUND_STATION_IP=192.168.144.12
SIYI_IP=192.168.144.25
SIYI_AI_IP=192.168.144.60
🎮 Camera Control CLI (cam_ctrl.py)
Run the Python CLI:

bash
Copy
Edit
python3 cam_ctrl.py
Available Keys (Numpad Layout)
Key	Action
0	Auto Centering
1	Follow Mode
2	Rotate Down
3	FPV Mode
4	Rotate Left
5	Stop Rotation
6	Rotate Right
7	Record Video
8	Rotate Up
9	Take Photo
v	Restart Video Feed
q	Quit

🔄 Restart Stream
Internally triggers:

bash
Copy
Edit
./restartVideo.sh
Ensure this script has executable permissions:

bash
Copy
Edit
chmod +x restartVideo.sh
📨 System Status Report (report.py)
This tool is designed to be run on boot and provides:

Ping check of key drone modules

RTSP stream integrity test

IP/interface diagnostics

Speedtest and latency

Sends a complete system report via email

Example:

bash
Copy
Edit
python3 report.py
Can be scheduled with cron, systemd, or a startup script.

🔐 Security
Store .env securely. Do not commit credentials to public repositories. Use .gitignore:

bash
Copy
Edit
.env
__pycache__/
🛠 Future Enhancements
Command macros for scan sequences

Autonomous gimbal sweep and loop modes

Optional web dashboard UI (Flask)


