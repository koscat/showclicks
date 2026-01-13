import socket, sys, threading, os, ctypes
import pystray
from PIL import Image

LOCK_PORT = 47654

def single_instance_or_exit():
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", LOCK_PORT))
    except:
        sys.exit()
    return s

def resource_path(name):
    if hasattr(sys, "_MEIPASS"):   # running from PyInstaller exe
        return os.path.join(sys._MEIPASS, name)
    return os.path.join(os.path.abspath("."), name)

def make_icon():
    try:
        img = Image.open(resource_path("icon.ico"))
        img = img.convert("RGBA")
        img = img.resize((32, 32), Image.LANCZOS)   # tray-safe size
        return img
    except Exception as e:
        print("Tray icon load failed:", e)
        return Image.new("RGBA", (32,32), (255,255,255,255))


def restart_as_admin():
    exe = sys.executable
    args = " ".join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", exe, args, None, 1
    )
    os._exit(0)

def start_tray(show_cb, exit_cb):
    def tray_thread():
        icon = pystray.Icon(
            "ShowClicks",
            make_icon(),
            "Show Clicks",
            menu=pystray.Menu(
                pystray.MenuItem("Show", lambda i: show_cb()),
                pystray.MenuItem("Restart as Administrator", lambda i: restart_as_admin()),
                pystray.MenuItem("Exit", lambda i: exit_cb()),
            )
        )
        icon.run()

    threading.Thread(target=tray_thread, daemon=True).start()