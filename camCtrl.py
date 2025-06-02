import subprocess
import signal

# Numpad-style mapping to C control indices
KEYMAP = {
    "0": (0, "Auto Centering"),
    "1": (20, "Follow Mode"),
    "2": (2, "Rotate Down"),
    "3": (21, "FPV Mode"),
    "4": (3, "Rotate Left"),
    "5": (5, "Stop Rotation"),
    "6": (4, "Rotate Right"),
    "7": (13, "Record Video"),
    "8": (1, "Rotate Up"),
    "9": (12, "Take Pictures")
}

RECORD_CMD = [
    "ffmpeg",
    "-rtsp_transport", "tcp",
    "-i", "rtsp://192.168.144.25:8554/main.264",
    "-c", "copy",
    "-f", "mp4",
    "output.mp4"
]

recording_proc = None

def print_menu():
    print("\n=== SIYI A8 Mini Camera Control (Numpad) ===")
    for k in sorted(KEYMAP.keys()):
        print(f" {k}: {KEYMAP[k][1]}")
    print(" -: Reboot GStreamer (restart video)")
    print(" +: Toggle Onboard Recording")
    print(" q: Quit")
    print("=" * 40)

def toggle_recording():
    global recording_proc
    if recording_proc and recording_proc.poll() is None:
        print("🟥 Stopping onboard recording...")
        recording_proc.terminate()
        recording_proc.wait()
        recording_proc = None
    else:
        print("🟩 Starting onboard recording...")
        recording_proc = subprocess.Popen(RECORD_CMD)

def restart_gstreamer():
    print("🔄 Rebooting GStreamer pipeline...")
    try:
        subprocess.run(["sudo", "systemctl", "stop", "usbcamera"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "usbcamera"], check=True)
        print("✅ GStreamer restarted.")
    except subprocess.CalledProcessError:
        print("❌ Failed to restart GStreamer.")

def main():
    while True:
        print_menu()
        key = input("Press key (0–9, +, -, q): ").strip().lower()

        if key == 'q':
            print("Exiting...")
            if recording_proc:
                print("Stopping active recording...")
                recording_proc.terminate()
                recording_proc.wait()
            break

        if key == '+':
            toggle_recording()
        elif key == '-':
            restart_gstreamer()
        elif key in KEYMAP:
            cmd_idx, label = KEYMAP[key]
            print(f"→ Executing: [{label}] → C Command Index [{cmd_idx}]")
            try:
                subprocess.run(["./A8miniCtrl", str(cmd_idx)], check=True)
            except subprocess.CalledProcessError:
                print("❌ Error running A8miniCtrl.")
            except FileNotFoundError:
                print("❌ 'A8miniCtrl' not found. Ensure it is compiled and in this directory.")
        else:
            print("❗ Invalid input. Use keys 0–9, +, -, or q.")

if __name__ == "__main__":
    main()
