import subprocess
import signal
import os
import shutil
import datetime
import sys

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

A8_BINARY = "./A8miniCtrl"
recording_proc = None

def check_requirements():
    if not os.path.isfile(A8_BINARY) or not os.access(A8_BINARY, os.X_OK):
        print(f"❌ '{A8_BINARY}' not found or not executable.")
        sys.exit(1)
    if shutil.which("ffmpeg") is None:
        print("❌ 'ffmpeg' not found. Please install it with: sudo apt install ffmpeg")
        sys.exit(1)

def print_menu():
    print("\n=== SIYI A8 Mini Camera Control (Numpad) ===")
    for k in sorted(KEYMAP.keys()):
        print(f" {k}: {KEYMAP[k][1]}")
    print(" -: Reboot GStreamer (restart video)")
    print(" +: Toggle Onboard Recording")
    print(" q: Quit")
    print("=" * 40)

def get_timestamped_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"recording_{timestamp}.mp4"

def toggle_recording():
    global recording_proc
    if recording_proc and recording_proc.poll() is None:
        print("🟥 Stopping onboard recording...")
        recording_proc.terminate()
        recording_proc.wait()
        recording_proc = None
    else:
        print("🟩 Starting onboard recording...")
        output_file = get_timestamped_filename()
        try:
            recording_proc = subprocess.Popen([
                "ffmpeg",
                "-rtsp_transport", "tcp",
                "-i", "rtsp://192.168.144.25:8554/main.264",
                "-c", "copy",
                "-f", "mp4",
                output_file
            ])
        except Exception as e:
            print(f"❌ Failed to start recording: {e}")
            recording_proc = None

def restart_gstreamer():
    print("🔄 Rebooting GStreamer pipeline...")
    try:
        subprocess.run(["sudo", "systemctl", "stop", "usbcamera"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "usbcamera"], check=True)
        print("✅ GStreamer restarted.")
    except subprocess.CalledProcessError:
        print("❌ Failed to restart GStreamer.")

def cleanup():
    global recording_proc
    if recording_proc and recording_proc.poll() is None:
        print("\n🛑 Stopping active recording before exit...")
        recording_proc.terminate()
        recording_proc.wait()
        recording_proc = None

def main():
    check_requirements()
    try:
        while True:
            print_menu()
            key = input("Press key (0–9, +, -, q): ").strip().lower()

            if key == 'q':
                print("Exiting...")
                break

            if key == '+':
                toggle_recording()
            elif key == '-':
                restart_gstreamer()
            elif key in KEYMAP:
                cmd_idx, label = KEYMAP[key]
                print(f"→ Executing: [{label}] → C Command Index [{cmd_idx}]")
                try:
                    subprocess.run([A8_BINARY, str(cmd_idx)], check=True)
                except subprocess.CalledProcessError:
                    print("❌ Error running A8miniCtrl.")
                except FileNotFoundError:
                    print(f"❌ '{A8_BINARY}' not found. Make sure it is compiled and in the directory.")
            else:
                print("❗ Invalid input. Use keys 0–9, +, -, or q.")
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user.")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
