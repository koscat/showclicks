import tkinter as tk
from tkinter import ttk, colorchooser
from pynput import mouse
import settings, autostart
import about

data = settings.load()
root = None
on_ui_ready = None

size = data["size"]
speed = data["speed"]
thick = data["thick"]
enabled = data["enabled"]

circle_enabled = data["circle_enabled"]
circle_color = data["circle_color"]
circle_size = data["circle_size"]
circle_alpha = data["circle_alpha"]
autostart_enabled = data["autostart"]

colors = {
    mouse.Button.left: data["colors"]["left"],
    mouse.Button.right: data["colors"]["right"],
    mouse.Button.middle: data["colors"]["middle"]
}

def save_all():
    settings.save({
        "size": size,
        "speed": speed,
        "thick": thick,
        "enabled": enabled,
        "circle_enabled": circle_enabled,
        "circle_color": circle_color,
        "circle_size": circle_size,
        "circle_alpha": circle_alpha,
        "autostart": autostart_enabled,
        "colors": {
            "left": colors[mouse.Button.left],
            "right": colors[mouse.Button.right],
            "middle": colors[mouse.Button.middle]
        }
    })

def start_ui():
    global root, size, speed, thick, enabled
    global circle_enabled, circle_color, circle_size, circle_alpha, autostart_enabled

    root = tk.Tk()
    root.title("Show Clicks")
    root.geometry("340x600")
    root.resizable(False, False)

    # hide instead of close
    root.protocol("WM_DELETE_WINDOW", root.withdraw)

    if on_ui_ready:
        on_ui_ready()

    enabled_var = tk.BooleanVar(value=enabled)
    circle_var = tk.BooleanVar(value=circle_enabled)
    auto_var = tk.BooleanVar(value=autostart_enabled)

    def set_size(v):  global size; size = int(float(v)); save_all()
    def set_speed(v): global speed; speed = float(v); save_all()
    def set_thick(v): global thick; thick = int(float(v)); save_all()
    def set_circle_size(v): global circle_size; circle_size = int(float(v)); save_all()
    def set_circle_alpha(v): global circle_alpha; circle_alpha = float(v); save_all()

    def toggle_enabled():
        global enabled; enabled = enabled_var.get(); save_all()
    def toggle_circle():
        global circle_enabled; circle_enabled = circle_var.get(); save_all()
    def toggle_autostart():
        global autostart_enabled
        autostart_enabled = auto_var.get()
        autostart.enable() if autostart_enabled else autostart.disable()
        save_all()

    def pick(btn):
        global enabled
        was = enabled; enabled = False
        c = colorchooser.askcolor(parent=root)[1]
        if c: colors[btn] = c; save_all()
        enabled = was

    def pick_circle():
        global circle_color
        c = colorchooser.askcolor(parent=root)[1]
        if c: circle_color = c; save_all()

    f = ttk.Frame(root, padding=15)
    f.pack(fill="both", expand=True)

    ttk.Label(f, text="Ripple Size").pack(anchor="w")
    s1 = ttk.Scale(f, from_=60, to=200, command=set_size)
    s1.set(size); s1.pack(fill="x")

    ttk.Label(f, text="Speed").pack(anchor="w", pady=(10,0))
    s2 = ttk.Scale(f, from_=0.005, to=0.05, command=set_speed)
    s2.set(speed); s2.pack(fill="x")

    ttk.Label(f, text="Thickness").pack(anchor="w", pady=(10,0))
    s3 = ttk.Scale(f, from_=1, to=10, command=set_thick)
    s3.set(thick); s3.pack(fill="x")

    ttk.Button(f, text="Left Click Color", underline=0,
               command=lambda: pick(mouse.Button.left)).pack(fill="x", pady=4)
    ttk.Button(f, text="Right Click Color", underline=0,
               command=lambda: pick(mouse.Button.right)).pack(fill="x", pady=4)
    ttk.Button(f, text="Middle Click Color", underline=0,
               command=lambda: pick(mouse.Button.middle)).pack(fill="x", pady=4)

    ttk.Checkbutton(f, text="Enabled", underline=0,
                    variable=enabled_var, command=toggle_enabled).pack(anchor="w", pady=6)

    ttk.Checkbutton(f, text="Start with Windows", underline=11,
                    variable=auto_var, command=toggle_autostart).pack(anchor="w", pady=4)

    ttk.Separator(f).pack(fill="x", pady=8)
    ttk.Label(f, text="Mouse Circle").pack(anchor="w")

    ttk.Checkbutton(f, text="Show Circle", underline=5,
                    variable=circle_var, command=toggle_circle).pack(anchor="w", pady=4)

    ttk.Label(f, text="Circle Size").pack(anchor="w")
    s4 = ttk.Scale(f, from_=10, to=80, command=set_circle_size)
    s4.set(circle_size); s4.pack(fill="x")

    ttk.Label(f, text="Circle Transparency").pack(anchor="w", pady=(10,0))
    s5 = ttk.Scale(f, from_=0.1, to=1.0, command=set_circle_alpha)
    s5.set(circle_alpha); s5.pack(fill="x")

    ttk.Button(f, text="Circle Color", underline=8,
               command=pick_circle).pack(fill="x", pady=4)
    ttk.Button(f, text="About", underline=0,
               command=lambda: about.show(root)).pack(fill="x", pady=5)

    # Alt shortcuts
    root.bind_all("<Alt-l>", lambda e: pick(mouse.Button.left))
    root.bind_all("<Alt-r>", lambda e: pick(mouse.Button.right))
    root.bind_all("<Alt-m>", lambda e: pick(mouse.Button.middle))
    root.bind_all("<Alt-e>", lambda e: enabled_var.set(not enabled_var.get()) or toggle_enabled())
    root.bind_all("<Alt-w>", lambda e: auto_var.set(not auto_var.get()) or toggle_autostart())
    root.bind_all("<Alt-c>", lambda e: circle_var.set(not circle_var.get()) or toggle_circle())
    root.bind_all("<Alt-o>", lambda e: pick_circle())
    root.bind_all("<Alt-a>", lambda e: about.show(root))

    root.mainloop()