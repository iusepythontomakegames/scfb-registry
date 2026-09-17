# winx — Windows extras (ext <winx>): beep / msgbox / speak / clip
import sys

VERSION = "1.0"


def on_load(rt):
    def _require_windows():
        if sys.platform != "win32":
            raise RuntimeError("winx only works on Windows")

    def beep(freq=800, ms=200):
        _require_windows()
        import winsound
        winsound.Beep(int(freq), int(ms))
        return freq

    def msgbox(text, title="SCFB basic"):
        _require_windows()
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, str(text), str(title), 0)
        return 0

    def speak(text):
        _require_windows()
        import subprocess
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Add-Type -AssemblyName System.Speech;"
             "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
             "$s.Speak([Console]::In.ReadToEnd())"],
            input=str(text), text=True, timeout=60)
        return text

    def clip(text):
        _require_windows()
        import subprocess
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Set-Clipboard -Value ([Console]::In.ReadToEnd())"],
            input=str(text), text=True, timeout=30)
        return text

    rt.register_ext_func("beep", beep)
    rt.register_ext_func("msgbox", msgbox)
    rt.register_ext_func("speak", speak)
    rt.register_ext_func("clip", clip)
