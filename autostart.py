import winreg, os, sys

APP_NAME = "ShowClicks"
EXE_PATH = os.path.abspath(sys.argv[0])

def enable():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, EXE_PATH)
    winreg.CloseKey(key)

def disable():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    try:
        winreg.DeleteValue(key, APP_NAME)
    except:
        pass
    winreg.CloseKey(key)