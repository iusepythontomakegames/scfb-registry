# sysx — system info extension (ext <sysx>)
import os as _os
import sys as _sys
import platform as _pf

VERSION = "1.0"


def on_load(rt):
    def ram():
        try:
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

            m = MS()
            m.dwLength = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return int(m.ullTotalPhys // (1024 * 1024))
        except Exception:
            return 0

    rt.register_ext_func("os_name", lambda: _pf.system() + " " + _pf.release())
    rt.register_ext_func("machine", lambda: _pf.machine())
    rt.register_ext_func("pyver", lambda: _sys.version.split()[0])
    rt.register_ext_func("cores", lambda: _os.cpu_count() or 1)
    rt.register_ext_func("ram", ram)
    rt.register_ext_func("cwd", lambda: _os.getcwd())
