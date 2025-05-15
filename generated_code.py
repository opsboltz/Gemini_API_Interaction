import pyautogui
import time
import threading
import sys
from pynput import keyboard

# --- Global Variables ---
clicking = False
holding = False
running = True

delay = 0.1
click_type = None

# --- Auto Clicker Thread ---
def auto_clicker():
    print("Auto-clicker thread started.")
    while running:
        if clicking:
            pyautogui.click()
            time.sleep(delay)
        else:
            time.sleep(0.05)
    print("Auto-clicker thread stopped.")

# --- Keyboard Handler ---
def on_press(key):
    global clicking, holding

    try:
        if key == keyboard.Key.f6:
            if click_type == 'auto':
                clicking = not clicking
                print(f"--- Auto-clicking {'STARTED' if clicking else 'STOPPED'} (Press F6 to toggle) ---")
            elif click_type == 'hold':
                holding = not holding
                if holding:
                    pyautogui.mouseDown(button='left')
                    print("--- Holding Left Click STARTED (Press F6 to release) ---")
                else:
                    pyautogui.mouseUp(button='left')
                    print("--- Holding Left Click RELEASED (Press F6 to hold again) ---")
    except Exception as e:
        print(f"[Key Error] {e}")

def on_release(key):
    return True  # Keep listener alive

# --- Main ---
if __name__ == "__main__":
    print("--- Python Autoclicker ---")
    print("Created by Craig for Steven")

    while click_type not in ['auto', 'hold']:
        choice = input("Choose mode: 'auto' or 'hold': ").strip().lower()
        if choice in ['auto', 'hold']:
            click_type = choice
        else:
            print("Invalid input.")

    if click_type == 'auto':
        while True:
            try:
                ms = int(input("Delay between clicks in ms (e.g., 100): "))
                if ms > 0:
                    delay = ms / 1000.0
                    break
                else:
                    print("Delay must be positive.")
            except ValueError:
                print("Enter a valid number.")

    print(f"\nMode: {click_type}")
    if click_type == 'auto':
        print(f"Delay: {delay}s")

    print("Move your mouse to the target.")
    print("Press F6 to toggle.")
    print("Press Ctrl+C to exit.\n" + "-"*30)

    if click_type == 'auto':
        t = threading.Thread(target=auto_clicker)
        t.daemon = True
        t.start()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    try:
        while True:
            time.sleep(0.1)  # Keeps main thread alive
    except KeyboardInterrupt:
        print("\n[Ctrl+C] Exiting...")
        running = False
        pyautogui.mouseUp(button='left')
        listener.stop()
        sys.exit(0)
