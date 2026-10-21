# SCFB basic extension — win32/64 API's
# ════════════════════════════════════════════════════════════════════════
# Call win32/64 API's from SCFB basic. Works for both win32 and win64 —
# the win32 API is the name, your OS does the 64-bit part.
#
# install (from PowerShell / Command Prompt):
#     py scfb_studio.py spm install win32
# use (in your program):
#     ext <win32>
#     print(w32ver())
#     w32box("hello from SCFB basic", "win32 says hi")
#
# spm registry entry:
#     {"name": "win32", "kind": "ext", "version": "1.0",
#      "file": "ext/win32.py", "desc": "call win32/64 API's"}
#
# functions (usable anywhere an expression is):
#     w32box(text, title)            message box — returns the button id
#     w32beep(freq, ms)              kernel32 Beep — returns true/false
#     w32sleep(ms)                   kernel32 Sleep — returns true
#     w32ticks()                     GetTickCount64 — ms since boot
#     w32proc()                      current process id
#     w32screen()                    GetSystemMetrics — "width,height"
#     w32mem()                       GlobalMemoryStatusEx — "total,free" MB
#     w32user()                      GetUserNameW — your username
#     w32comp()                      GetComputerNameW — computer name
#     w32env(name)                   GetEnvironmentVariableW — env var
#     w32ver()                       RtlGetVersion — "major.minor.build"
#     w32regread(root, subkey, name) read a registry value
#                                    (HKCR/HKCU/HKLM/HKU/HKPD/HKCC)
#     w32regwrite(root, subkey, name, value)  write one (SZ or DWORD)
#     w32call(dll, func, args...)     raw call, any dll, int result
#     w32callstr(dll, func, args...)  raw call that returns a wide string
#
# strings are passed as wide (UTF-16) pointers, ints as plain numbers.
# Some API's are crimes and have been arrested. cry about it.

import ctypes
import struct
import sys

_PLATFORM_ERR = ("win32/64 API's need windows. this machine is not "
                  "windows. cry about it.")

# taking the whole box (or someone else's box) down is not allowed
CRIMES = (
    "ExitWindows", "ExitWindowsEx",
    "InitiateSystemShutdown", "InitiateSystemShutdownEx",
    "NtShutdownSystem", "NtRaiseHardError", "NtSetSystemEnvironmentValue",
    "NtSystemDebugControl", "RtlSetProcessIsCritical",
    "SetSystemPowerState", "WriteConsoleInput",
)

_REG_ROOTS = {
    "HKCR": 0x80000000, "HKEY_CLASSES_ROOT": 0x80000000,
    "HKCU": 0x80000001, "HKEY_CURRENT_USER": 0x80000001,
    "HKLM": 0x80000002, "HKEY_LOCAL_MACHINE": 0x80000002,
    "HKU": 0x80000003, "HKEY_USERS": 0x80000003,
    "HKPD": 0x80000004, "HKEY_PERFORMANCE_DATA": 0x80000004,
    "HKCC": 0x80000005, "HKEY_CURRENT_CONFIG": 0x80000005,
}


class _MemStatus(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


class _OsVersionInfoW(ctypes.Structure):
    _fields_ = [("dwOSVersionInfoSize", ctypes.c_ulong),
                ("dwMajorVersion", ctypes.c_ulong),
                ("dwMinorVersion", ctypes.c_ulong),
                ("dwBuildNumber", ctypes.c_ulong),
                ("dwPlatformId", ctypes.c_ulong),
                ("szCSDVersion", ctypes.c_wchar * 128)]


def _guard(func):
    if func in CRIMES:
        raise RuntimeError("CRIME DETECTED: %s would take the whole box "
                           "down. denied. cry about it." % func)
    if sys.platform != "win32":
        raise RuntimeError(_PLATFORM_ERR)


def _call(dll, func, args, restype):
    _guard(func)
    fn = getattr(ctypes.windll[str(dll)], str(func))
    fn.restype = restype
    conv = []
    for a in args:
        if isinstance(a, bool):
            conv.append(int(a))
        elif a is None:
            conv.append(0)
        elif isinstance(a, float):
            conv.append(int(a))
        else:
            conv.append(a)  # int passes raw, str passes as wide (UTF-16)
    return fn(*conv)


# ── raw calls ────────────────────────────────────────────────────────────

def w32call(dll, func, *args):
    """w32call("user32", "GetSystemMetrics", 0) → int"""
    return _call(dll, func, args, ctypes.c_longlong)


def w32callstr(dll, func, *args):
    """w32callstr("kernel32", "GetCommandLineW") → wide string"""
    return _call(dll, func, args, ctypes.c_wchar_p) or ""


# ── conveniences (all built on real API calls) ───────────────────────────

def w32box(text, title="SCFB basic"):
    """MessageBoxW — returns 1 (ok), 2 (cancel), 6 (yes), 7 (no)..."""
    return _call("user32", "MessageBoxW",
                 (0, str(text), str(title), 0), ctypes.c_longlong)


def w32beep(freq, ms):
    """kernel32 Beep — true when the beep beeped"""
    return bool(_call("kernel32", "Beep",
                      (int(freq), int(ms)), ctypes.c_longlong))


def w32sleep(ms):
    """kernel32 Sleep — waits, then returns true"""
    _call("kernel32", "Sleep", (int(ms),), ctypes.c_longlong)
    return True


def w32ticks():
    """GetTickCount64 — milliseconds since boot"""
    return _call("kernel32", "GetTickCount64", (), ctypes.c_ulonglong)


def w32proc():
    """GetCurrentProcessId"""
    return _call("kernel32", "GetCurrentProcessId", (), ctypes.c_ulong)


def w32screen():
    """GetSystemMetrics — screen size as W,H (a string)"""
    w = _call("user32", "GetSystemMetrics", (0,), ctypes.c_longlong)
    h = _call("user32", "GetSystemMetrics", (1,), ctypes.c_longlong)
    return "%d,%d" % (w, h)


def w32mem():
    """GlobalMemoryStatusEx — RAM as "total,free" in MB"""
    _guard("GlobalMemoryStatusEx")
    st = _MemStatus()
    st.dwLength = ctypes.sizeof(_MemStatus)
    ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
    if not ok:
        raise RuntimeError("GlobalMemoryStatusEx refused. win32 error %d"
                           % ctypes.GetLastError())
    return "%d,%d" % (st.ullTotalPhys // (1024 * 1024),
                      st.ullAvailPhys // (1024 * 1024))


def w32user():
    """GetUserNameW — your username"""
    _guard("GetUserNameW")
    buf = ctypes.create_unicode_buffer(512)
    n = ctypes.c_ulong(512)
    ok = ctypes.windll.advapi32.GetUserNameW(buf, ctypes.byref(n))
    if not ok:
        raise RuntimeError("GetUserNameW refused. win32 error %d"
                           % ctypes.GetLastError())
    return buf.value


def w32comp():
    """GetComputerNameW — the machine's DNS name"""
    _guard("GetComputerNameW")
    buf = ctypes.create_unicode_buffer(512)
    n = ctypes.c_ulong(512)
    ok = ctypes.windll.kernel32.GetComputerNameW(0, buf, ctypes.byref(n))
    if not ok:
        raise RuntimeError("GetComputerNameW refused. win32 error %d"
                           % ctypes.GetLastError())
    return buf.value


def w32env(name):
    """GetEnvironmentVariableW — an environment variable's value"""
    _guard("GetEnvironmentVariableW")
    buf = ctypes.create_unicode_buffer(32768)
    n = ctypes.windll.kernel32.GetEnvironmentVariableW(str(name), buf, 32768)
    if n == 0:
        raise RuntimeError("there is no %r in the environment. cry about it."
                           % str(name))
    return buf.value


def w32ver():
    """RtlGetVersion — Windows version as major.minor.build"""
    _guard("RtlGetVersion")
    vi = _OsVersionInfoW()
    vi.dwOSVersionInfoSize = ctypes.sizeof(_OsVersionInfoW)
    rc = ctypes.windll.ntdll.RtlGetVersion(ctypes.byref(vi))
    if rc != 0:
        raise RuntimeError("RtlGetVersion refused: %d" % rc)
    return "%d.%d.%d" % (vi.dwMajorVersion, vi.dwMinorVersion,
                         vi.dwBuildNumber)


# ── registry ─────────────────────────────────────────────────────────────

def _regroot(root):
    r = _REG_ROOTS.get(str(root).upper())
    if r is None:
        raise RuntimeError("registry root %r is not one of %s"
                           % (str(root), "/".join(sorted(set(
                               k for k in _REG_ROOTS if len(k) == 4)))))
    return r


def w32regread(root, subkey, name):
    """RegGetValueW — reads SZ/DWORD/QWORD values, returns str or int"""
    hroot = _regroot(root)          # argument check first...
    _guard("RegGetValueW")          # ...then the windows check
    dwType = ctypes.c_ulong(0)
    buf = ctypes.create_string_buffer(4096)
    cb = ctypes.c_ulong(ctypes.sizeof(buf))
    rc = ctypes.windll.advapi32.RegGetValueW(
        hroot, str(subkey), str(name), 0x0000FFFF,  # RRF_RT_ANY
        ctypes.byref(dwType), buf, ctypes.byref(cb))
    if rc != 0:
        raise RuntimeError("regread refused. win32 error %d "
                           "(key there? name there? exactly. cry about it.)" % rc)
    raw = buf.raw
    t = dwType.value
    if t in (1, 2):  # REG_SZ / REG_EXPAND_SZ
        return raw.decode("utf-16-le", errors="replace").split("\x00")[0]
    if t == 4:  # REG_DWORD
        return struct.unpack("<i", raw[:4])[0]
    if t == 11:  # REG_QWORD
        return struct.unpack("<q", raw[:8])[0]
    if t == 3:  # REG_BINARY
        return (raw[:cb.value]).hex()
    raise RuntimeError("registry type %d is too exotic. cry about it." % t)


def w32regwrite(root, subkey, name, value):
    """RegCreateKeyExW + RegSetValueExW — writes SZ (str) or DWORD (int)"""
    hroot = _regroot(root)          # argument check first...
    _guard("RegSetValueExW")        # ...then the windows check
    hkey = ctypes.c_void_p(0)
    rc = ctypes.windll.advapi32.RegCreateKeyExW(
        hroot, str(subkey), 0, None, 0, 0x0002,  # KEY_SET_VALUE
        None, ctypes.byref(hkey), None)
    if rc != 0:
        raise RuntimeError("regwrite refused. win32 error %d" % rc)
    try:
        if isinstance(value, str):
            data = ctypes.create_unicode_buffer(str(value))
            rc = ctypes.windll.advapi32.RegSetValueExW(
                hkey, str(name), 0, 1,  # REG_SZ
                ctypes.cast(data, ctypes.c_void_p), ctypes.sizeof(data))
        else:
            data = struct.pack("<I", int(value) & 0xFFFFFFFF)
            rc = ctypes.windll.advapi32.RegSetValueExW(
                hkey, str(name), 0, 4,  # REG_DWORD
                data, len(data))
        if rc != 0:
            raise RuntimeError("RegSetValueExW refused. win32 error %d" % rc)
    finally:
        ctypes.windll.advapi32.RegCloseKey(hkey)
    return True


# ── SCFB basic hookup ────────────────────────────────────────────────────

def on_load(rt):
    rt.register_ext_func("w32call", w32call)
    rt.register_ext_func("w32callstr", w32callstr)
    rt.register_ext_func("w32box", w32box)
    rt.register_ext_func("w32beep", w32beep)
    rt.register_ext_func("w32sleep", w32sleep)
    rt.register_ext_func("w32ticks", w32ticks)
    rt.register_ext_func("w32proc", w32proc)
    rt.register_ext_func("w32screen", w32screen)
    rt.register_ext_func("w32mem", w32mem)
    rt.register_ext_func("w32user", w32user)
    rt.register_ext_func("w32comp", w32comp)
    rt.register_ext_func("w32env", w32env)
    rt.register_ext_func("w32ver", w32ver)
    rt.register_ext_func("w32regread", w32regread)
    rt.register_ext_func("w32regwrite", w32regwrite)
