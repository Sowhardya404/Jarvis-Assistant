import os

# ✅ Volume Control
def increase_volume():
    os.system(r"C:\nircmd-x64\nircmd.exe changesysvolume 5000")

def decrease_volume():
    os.system(r"C:\nircmd-x64\nircmd.exe changesysvolume -5000")
    
# ✅ Brightness Control
def increase_brightness():
    try:
        import screen_brightness_control as sbc
        current = sbc.get_brightness(display=0)[0]
        sbc.set_brightness(min(current + 10, 100), display=0)
    except Exception as e:
        print(f"Brightness up error: {e}")

def decrease_brightness():
    try:
        import screen_brightness_control as sbc
        current = sbc.get_brightness(display=0)[0]
        sbc.set_brightness(max(current - 10, 0), display=0)
    except Exception as e:
        print(f"Brightness down error: {e}")

def open_application(app_name):
    app_name = app_name.lower()

    # Handle Notepad
    if "notepad" in app_name:
        try:
            os.system("notepad.exe")
            return "Opening Notepad."
        except Exception as e:
            return f"Could not open Notepad. Error: {e}"

    # Handle Calculator
    elif "calculator" in app_name or "calc" in app_name:
        try:
            os.system("calc.exe")
            return "Opening Calculator."
        except Exception as e:
            return f"Could not open Calculator. Error: {e}"

    # Handle folders (e.g., Documents, Downloads, D drive, etc.)
    else:
        # Attempt to open folder path based on command
        folders = {
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
            "videos": os.path.join(os.path.expanduser("~"), "Videos"),
            "music": os.path.join(os.path.expanduser("~"), "Music"),
            "d drive": "D:\\",
            "c drive": "C:\\"
        }

        for key in folders:
            if key in app_name:
                path = folders[key]
                try:
                    os.startfile(path)
                    return f"Opening {key}."
                except Exception as e:
                    return f"Could not open {key}. Error: {e}"

        return "Sorry, I can only open Notepad, Calculator, or known folders like Downloads or D drive."
