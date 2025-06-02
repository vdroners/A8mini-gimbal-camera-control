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

# Path to shell scripts
RECORD_SCRIPT = "./recordLocal.sh"
RESTART_GST_SCRIPT = "./restartVideo.sh"

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
        recording_proc = subprocess.Popen([RECORD_SCRIPT])

def restart_gstreamer():
    print("🔄 Rebooting GStreamer via restartVideo.sh...")
    try:
        subprocess.run([RESTART_GST_SCRIPT], check=True)
        print("✅ GStreamer rebooted.")
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
                subprocess.run(["./A8miniControl", str(cmd_idx)], check=True)
            except subprocess.CalledProcessError:
                print("❌ Error running A8miniControl.")
        else:
            print("❗ Invalid input. Use keys 0–9, +, -, or q.")

if __name__ == "__main__":
    main()
