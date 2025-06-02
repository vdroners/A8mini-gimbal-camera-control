import subprocess

# Numpad-style control mapping to C command indices
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

def print_menu():
    print("\n=== SIYI A8 Mini Camera Control (Numpad Mapped) ===")
    for k in sorted(KEYMAP.keys()):
        print(f" {k}: {KEYMAP[k][1]}")
    print(" q: Quit")
    print("=" * 40)

def main():
    while True:
        print_menu()
        key = input("Press key (0–9 or q): ").strip().lower()
        if key == 'q':
            print("Exiting...")
            break
        if key in KEYMAP:
            cmd_idx, label = KEYMAP[key]
            print(f"→ Executing: [{label}] → C Command Index [{cmd_idx}]")
            try:
                subprocess.run(["./A8miniControl", str(cmd_idx)], check=True)
            except subprocess.CalledProcessError:
                print("❌ Error running A8miniControl.")
        else:
            print("❗ Invalid input. Use keys 0–9 or q.")

if __name__ == "__main__":
