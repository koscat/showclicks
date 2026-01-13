import tkinter as tk
import webbrowser

REPO_URL = "https://github.com/koscat/showclicks/"
RELEASES_URL = "https://github.com/koscat/showclicks/releases"

def show(parent):
    w = tk.Toplevel(parent)
    w.title("About")
    w.geometry("300x260")
    w.resizable(False, False)

    tk.Label(w, text="Show Clicks", font=("Segoe UI", 12, "bold")).pack(pady=6)
    tk.Label(w, text="Version 1.0").pack()
    tk.Label(w, text="Developed by Kaushik").pack()

    def make_link(text, url):
        lbl = tk.Label(w, text=text, fg="blue", cursor="hand2", wraplength=260, justify="center")
        lbl.pack(pady=4)
        lbl.bind("<Button-1>", lambda e: webbrowser.open(url))

    make_link("Source Code:\n" + REPO_URL, REPO_URL)
    make_link("Check for Updates", RELEASES_URL)

    tk.Label(w, text="Copyright (c) 2026 Kaushik").pack(pady=8)

# ---------------- Developer Notes ----------------
# This project is open and free to use.
# Feel free to modify, remix, or rebuild it in your own way.
# Credit is appreciated.
# -----------------------------------------------