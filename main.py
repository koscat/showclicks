from pynput import mouse
import tkinter as tk
import ui
import ctypes
import tray
import sys

# ---- startup flag ----
STARTUP = "--startup" in sys.argv

# ---- single instance ----
lock = tray.single_instance_or_exit()

circle_win = None
circle_canvas = None
last_pos = (0, 0)

# Invisible magic color (almost black, but not black)
MAGIC = "#010101"
SAFE_BLACK = "#000000"

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20

def root_alive():
    try:
        return ui.root and ui.root.winfo_exists()
    except:
        return False

def safe_color(c):
    if not c:
        return SAFE_BLACK
    if c.lower() == MAGIC:
        return SAFE_BLACK
    return c

def make_click_through(win):
    hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(
        hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT
    )

def ensure_circle():
    global circle_win, circle_canvas
    if circle_win or not root_alive():
        return
    root = ui.root
    circle_win = tk.Toplevel(root)
    circle_win.overrideredirect(True)
    circle_win.attributes("-topmost", True)
    circle_win.attributes("-transparentcolor", MAGIC)
    circle_canvas = tk.Canvas(circle_win, bg=MAGIC, highlightthickness=0)
    circle_canvas.pack(fill="both", expand=True)
    circle_win.update_idletasks()
    make_click_through(circle_win)

def update_circle():
    if not root_alive():
        return

    if not ui.circle_enabled:
        if circle_win:
            try: circle_win.withdraw()
            except: pass
        ui.root.after(1, update_circle)
        return

    ensure_circle()
    if not circle_win:
        ui.root.after(1, update_circle)
        return

    try:
        circle_win.deiconify()
        x, y = last_pos
        s = ui.circle_size
        circle_win.geometry(f"{s}x{s}+{x-s//2}+{y-s//2}")
        circle_canvas.config(width=s, height=s)
        circle_canvas.delete("all")

        col = safe_color(ui.circle_color)

        circle_canvas.create_oval(
            1, 1, s-1, s-1,
            outline=col,
            fill=col,
            width=2
        )
        circle_win.attributes("-alpha", ui.circle_alpha)
    except:
        pass

    ui.root.after(1, update_circle)

def ripple(x, y, color):
    if not root_alive():
        return
    try:
        win = tk.Toplevel(ui.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.attributes("-transparentcolor", MAGIC)
        s = ui.size
        win.geometry(f"{s}x{s}+{x-s//2}+{y-s//2}")
        c = tk.Canvas(win, width=s, height=s, bg=MAGIC, highlightthickness=0)
        c.pack()

        col = safe_color(color)

        cx = cy = s // 2
        r = 2
        maxr = s // 2 - 15
        circ = c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=col, width=ui.thick)
        steps = 15
        step = 0

        def anim():
            nonlocal step
            if step >= steps or not win.winfo_exists():
                try: win.destroy()
                except: pass
                return
            r = int((maxr / steps) * (step + 1))
            c.coords(circ, cx-r, cy-r, cx+r, cy+r)
            win.attributes("-alpha", 1 - (step / steps))
            step += 1
            win.after(int(ui.speed * 1000), anim)
        anim()
    except:
        pass

def on_click(x, y, b, p):
    if p and ui.enabled and root_alive():
        col = safe_color(ui.colors.get(b, SAFE_BLACK))
        ui.root.after(0, lambda: ripple(x, y, col))

def on_move(x, y):
    global last_pos
    last_pos = (x, y)

mouse.Listener(on_click=on_click, on_move=on_move).start()

def start_circle():
    if root_alive():
        ui.root.after(1, update_circle)

def show_ui():
    if root_alive():
        ui.root.deiconify()

def exit_app():
    try:
        if root_alive():
            ui.root.destroy()
    except:
        pass

# ---- start app ----
def ui_ready():
    start_circle()
    tray.start_tray(show_ui, exit_app)
    if STARTUP and root_alive():
        ui.root.withdraw()   # silent startup

ui.on_ui_ready = ui_ready
ui.start_ui()