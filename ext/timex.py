# timex — time extension (ext <timex>)
import time as _t

VERSION = "1.0"


def on_load(rt):
    if getattr(rt, "_t0", None) is None:
        rt._t0 = _t.time()

    def delay(ms):
        ms = max(0.0, min(float(ms), 30000.0))
        _t.sleep(ms / 1000.0)
        return int(ms)

    def wait(s):
        s = max(0.0, min(float(s), 30.0))
        _t.sleep(s)
        return s

    rt.register_ext_func("now", lambda: int(_t.time()))
    rt.register_ext_func("clock", lambda: round(_t.time() - rt._t0, 3))
    rt.register_ext_func("delay", delay)
    rt.register_ext_func("wait", wait)
    rt.register_ext_func("year", lambda: _t.localtime().tm_year)
    rt.register_ext_func("month", lambda: _t.localtime().tm_mon)
    rt.register_ext_func("day", lambda: _t.localtime().tm_mday)
    rt.register_ext_func("hour", lambda: _t.localtime().tm_hour)
    rt.register_ext_func("minute", lambda: _t.localtime().tm_min)
    rt.register_ext_func("second", lambda: _t.localtime().tm_sec)
