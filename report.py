import os
import time
import psutil
import socket
import subprocess
import smtplib
from dotenv import load_dotenv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import mimetypes

load_dotenv()
time.sleep(20)

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(',')

AIRCRAFT_NAME = os.getenv("AIRCRAFT_NAME")
SERIAL_NUMBER = os.getenv("SERIAL_NUMBER")
FAA_REGISTRATION = os.getenv("FAA_REGISTRATION")
TAIL_NUMBER = os.getenv("TAIL_NUMBER")

RESTREAM_URL = os.getenv("RESTREAM_URL")
SIYI_RTSP = os.getenv("SIYI_RTSP")

AIR_DATA_TX_IP = os.getenv("AIR_DATA_TX_IP")
GROUND_STATION_IP = os.getenv("GROUND_STATION_IP")
SIYI_IP = os.getenv("SIYI_IP")
SIYI_AI_IP = os.getenv("SIYI_AI_IP")
NOSE_CAM_IP = os.getenv("NOSE_CAM_IP")

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return f"{int(f.read())/1000:.1f}°C"
    except:
        return "Unavailable"

def get_uptime():
    return datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

def get_disk_usage():
    usage = psutil.disk_usage('/')
    return f"{usage.percent}% used of {usage.total // (2**30)}GB"

def get_load_average():
    return ', '.join(f"{x:.2f}" for x in os.getloadavg())

def get_public_ip():
    try:
        return subprocess.check_output(["curl", "-s", "-m", "2", "https://ifconfig.me"], text=True).strip()
    except:
        return "Unavailable"

def list_usb_devices():
    try:
        return subprocess.check_output(["lsusb"], text=True)
    except:
        return "Unavailable"

def get_zerotier_status():
    try:
        info = subprocess.check_output(["zerotier-cli", "info"], text=True).strip()
        networks = subprocess.check_output(["zerotier-cli", "listnetworks"], text=True).strip().splitlines()
        parsed = ""
        for line in networks:
            if not line.startswith("200") or len(line.split()) < 8:
                continue
            parts = line.split()
            nwid = parts[2]
            name = parts[3]
            status = parts[5]
            interface = parts[7]
            ip = parts[8] if len(parts) > 8 else "No IP"
            parsed += f"<b>{name}</b> ({nwid}): {ip} on <i>{interface}</i> - <span style='color:green'>{status}</span><br>"
        return f"{info}<br>{parsed}"
    except Exception as e:
        return f"Unavailable ({e})"

def get_gstreamer_status():
    try:
        subprocess.check_output("pgrep -f gst-launch-1.0", shell=True)
        return "Active"
    except:
        return "Inactive"

def check_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except:
        return False

def ping_host(ip):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "2", ip], stderr=subprocess.DEVNULL)
        return "<span style='color:green'>Reachable</span>"
    except:
        return "<span style='color:red'>Unreachable</span>"

def check_rtsp_stream(rtsp_url):
    try:
        subprocess.run(
            ["ffprobe", "-v", "error", "-rtsp_transport", "tcp", "-i", rtsp_url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5
        )
        return "<span style='color:green'>Online</span>"
    except:
        return "<span style='color:red'>Offline</span>"

def get_active_ssh():
    try:
        output = subprocess.check_output("who", text=True)
        return "<br>".join(line for line in output.splitlines() if "ssh" in line) or "None"
    except:
        return "Unavailable"

def get_speedtest():
    try:
        output = subprocess.check_output(["speedtest-cli", "--secure"], text=True, timeout=30)
        lines = output.strip().splitlines()
        ping = download = upload = isp = ""

        for line in lines:
            if "Testing from" in line:
                isp = line.replace("Testing from", "").strip()
            elif "Hosted by" in line:
                ping = line.strip()
            elif "Download:" in line:
                download = line.strip()
            elif "Upload:" in line:
                upload = line.strip()

        return f"""
<b>ISP:</b> {isp}<br>
<b>{ping}</b><br>
<b>{download}</b><br>
<b>{upload}</b><br>
""".strip()
    except:
        return "Unavailable"

def capture_rtsp_frame(rtsp_url, filename):
    try:
        temp_video = "temp_video.mp4"
        subprocess.run(["ffmpeg", "-rtsp_transport", "tcp", "-i", rtsp_url, "-t", "1", "-c:v", "copy", temp_video, "-y"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        subprocess.run(["ffmpeg", "-i", temp_video, "-frames:v", "1", "-q:v", "2", filename, "-y"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        os.remove(temp_video)
        return filename if os.path.exists(filename) else None
    except:
        return None

def build_report():
    return f"""
<h2>📡 Aircraft Info</h2>
<b>Name:</b> {AIRCRAFT_NAME}<br>
<b>Serial #:</b> {SERIAL_NUMBER}<br>
<b>FAA Registration:</b> {FAA_REGISTRATION}<br>
<b>Tail #:</b> {TAIL_NUMBER}<br><br>

<h2>🖥️ System Status</h2>
<b>Uptime:</b> {get_uptime()}<br>
<b>CPU Usage:</b> {psutil.cpu_percent(interval=1)}%<br>
<b>Memory Usage:</b> {psutil.virtual_memory().percent}%<br>
<b>Temperature:</b> {get_temp()}<br>
<b>Disk Usage:</b> {get_disk_usage()}<br>
<b>Load Average:</b> {get_load_average()}<br>
<b>Public IP:</b> {get_public_ip()}<br><br>

<h2>🔧 Service Status</h2>
<b>GStreamer:</b> {get_gstreamer_status()}<br>
<b>ZeroTier:</b><br>{get_zerotier_status()}<br>
<b>Restream Camera:</b> {check_rtsp_stream(RESTREAM_URL)}<br><br>

<h2>📶 Ping Status</h2>
<b>Air Data TX:</b> {AIR_DATA_TX_IP} {ping_host(AIR_DATA_TX_IP)}<br>
<b>Ground Station:</b> {GROUND_STATION_IP} {ping_host(GROUND_STATION_IP)}<br>
<b>SIYI A8 Mini:</b> {SIYI_IP} {ping_host(SIYI_IP)}<br>
<b>SIYI AI Module:</b> {SIYI_AI_IP} {ping_host(SIYI_AI_IP)}<br>
<b>Nose Camera:</b> {NOSE_CAM_IP} {ping_host(NOSE_CAM_IP)}<br><br>

<h2>🔐 SSH Sessions</h2>
{get_active_ssh()}<br><br>

<h2>🔌 USB Devices</h2>
<pre>{list_usb_devices()}</pre>

<h2>🌐 Internet Speed Test</h2>
{get_speedtest()}
"""

def send_email():
    html_report = build_report()
    attachments = []

    if check_rtsp_stream(SIYI_RTSP).find("Online") != -1:
        siyi_img = capture_rtsp_frame(SIYI_RTSP, "siyi.jpg")
        if siyi_img and os.path.exists(siyi_img):
            with open(siyi_img, "rb") as img:
                mime_type, _ = mimetypes.guess_type(siyi_img)
                if mime_type:
                    attachments.append(("Siyi_Cam.jpg", MIMEImage(img.read(), _subtype=mime_type.split("/")[1])))

    if check_rtsp_stream(RESTREAM_URL).find("Online") != -1:
        restream_img = capture_rtsp_frame(RESTREAM_URL, "restream.jpg")
        if restream_img and os.path.exists(restream_img):
            with open(restream_img, "rb") as img:
                mime_type, _ = mimetypes.guess_type(restream_img)
                if mime_type:
                    attachments.append(("RPi_Restream.jpg", MIMEImage(img.read(), _subtype=mime_type.split("/")[1])))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)

            for recipient in EMAIL_RECIPIENTS:
                msg = MIMEMultipart()
                msg["From"] = EMAIL_SENDER
                msg["To"] = recipient
                msg["Subject"] = f"{AIRCRAFT_NAME} - Boot Report @ {datetime.now().strftime('%H:%M:%S')}"
                msg.attach(MIMEText(html_report, "html"))

                for filename, image in attachments:
                    image.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(image)

                server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
                print(f"Email sent to {recipient}")

    except Exception as e:
        print(f"Failed to send email: {e}")

    for f in ("siyi.jpg", "restream.jpg"):
        try:
            os.remove(f)
        except:
            pass

if __name__ == "__main__":
    send_email()
